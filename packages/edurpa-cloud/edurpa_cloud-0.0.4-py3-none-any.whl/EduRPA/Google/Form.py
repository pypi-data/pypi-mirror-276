import io
import re
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from robot.api.deco import keyword, not_keyword
from googleapiclient.http import MediaIoBaseDownload
import random

class Form:
    def __init__(self):
        self.creds=None
    
    @keyword("Set Up Form Connection")
    def authenticate(self, token_file_path: str=None):
        if not token_file_path:
            raise {'error': 'Not found credential file'}

        with open(token_file_path, 'r') as file:
            data = json.load(file)
            
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        token_uri = data['token_uri']
        client_id = data['client_id']
        client_secret = data['client_secret']
        scopes = data['scopes']
        
        self.creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes
        )
        
        if not self.creds.valid:
            self.creds.refresh(Request())
            
        return self.creds

    @keyword("Create Form")
    def create_new_form(self, title):
        if not self.creds:
            return {'error': 'Authentication failed'}

        try:
            service = build('forms', 'v1', credentials=self.creds)
            form_body = {
                'info': {
                    'title': title,
                    'documentTitle': title,
                },
            }
            result = service.forms().create(body=form_body).execute()
            
            update = {
                "requests": [
                    {
                        "updateSettings": {
                            "settings": {"quizSettings": {"isQuiz": True}},
                            "updateMask": "quizSettings.isQuiz",
                        }
                    }
                ]
            }

            # Converts the form into a quiz
            service.forms().batchUpdate(formId=result["formId"], body=update).execute()

            # Print the result to see it's now a quiz
            getresult = service.forms().get(formId=result["formId"]).execute()
            return getresult["formId"]
        
        except HttpError as error:
            return {'error': str(error), 'error_details': error.error_details}
        
    
    @keyword("Get Google Doc ID")
    def get_doc_id_from_url(self, url):
        """Extracts and returns the Google Drive document ID from the given URL."""
        pattern = r"https://docs\.google\.com/document/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None

    @keyword("Read Google Doc Content")
    def read_google_doc_content(self, doc_id):
        """Reads content from a Google Docs document."""
        if not self.creds:
            return {'error': 'Authentication failed'}

        try:
            service = build('drive', 'v3', credentials=self.creds)
            request = service.files().export_media(fileId=doc_id, mimeType='text/plain')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            return fh.getvalue().decode()
        except HttpError as error:
            return {'error': str(error), 'error_details': error.error_details}
        
    @not_keyword
    def parse_questions(self, content):
        pattern = r'Câu (\d+)\.\s*(.*?)\s*A\.\s*(.*?)\s*B\.\s*(.*?)\s*C\.\s*(.*?)\s*D\.\s*(.*?)(?=\s*Câu|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        if not matches:
            return None  # Return None or an empty list if no matches are found
        
        questions = []
        for match in matches:
            if len(match) < 6:
                continue
            title = 'Câu ' + match[0] + '. ' + ' '.join(match[1].split())
            question = {
                'title': title,
                'options': [' '.join(option.split()) for option in match[2:]]
            }
            questions.append(question)
        return questions
    
    @not_keyword
    def parse_answer_keys(self, answers_content):
        pattern = r'(\d+)\.([A-D])'
        answer_matches = re.findall(pattern, answers_content)
        answer_keys = {num: ans for num, ans in answer_matches}
        return answer_keys
        
    @keyword("Read Google Doc Content And Answers")
    def read_google_doc_content_and_answers(self, doc_id):
        content = self.read_google_doc_content(doc_id)
    
        if 'error' in content:
            return content  # Return error if reading failed

        # Use regex to split the content based on variations of the delimiter
        parts = re.split(r'-{1,}HẾT-{1,}', content, flags=re.IGNORECASE)
        doc_content = parts[0].strip() if len(parts) > 0 else ""
        answers_content = parts[1].strip() if len(parts) > 1 else ""
        
        
        questions = self.parse_questions(doc_content)
        # Parse the answer keys
        answer_keys = self.parse_answer_keys(answers_content)
    
                
        return questions, answer_keys

    @not_keyword
    def convertCorrectOptionToIndex(self, option):
        if option == 'A':
            return 0
        elif option == 'B':
            return 1
        elif option == 'C':
            return 2
        elif option == 'D':
            return 3
        else:
            return -1

    @keyword("Add Questions To Form")
    def add_questions_to_form(self, form_id, questions):
        if not self.creds:
            return {'error': 'Authentication failed'}

        if not questions:  # Check if there are no questions to add
            return {'error': 'No questions parsed from the document'}

        try:
            service = build('forms', 'v1', credentials=self.creds)
            requests = []
            for question in reversed(questions):
                if 'correct_answer' not in question or question['correct_answer'] is None:
                    # Randomly assign a correct answer if none is specified
                    correct_option_index = random.randint(0, len(question['options']) - 1)
                else:
                    correct_option_index = self.convertCorrectOptionToIndex(question['correct_answer'])

                unique_options = list(set(question['options']))  # Remove duplicate options
                if len(unique_options) != len(question['options']):
                    continue  # Skip adding this question if duplicates were removed

                choiceQuestion = {
                    'type': 'RADIO',
                    'options': [{'value': choice} for choice in unique_options],
                }

                if correct_option_index < 0 or correct_option_index >= len(unique_options):
                    continue

                new_question = {
                    'createItem': {
                        'item': {
                            'title': question['title'],
                            'questionItem': {
                                'question': {
                                    'required': True,
                                    'choiceQuestion': choiceQuestion,
                                    "grading": {
                                        "pointValue": 1,
                                        "correctAnswers": {
                                            "answers": [choiceQuestion['options'][correct_option_index]]
                                        },
                                        "whenRight": {"text": "You got it!"},
                                        "whenWrong": {"text": "Sorry, that's wrong"}
                                    },
                                }
                            }
                        },
                        'location': {
                            'index': 0
                        }
                    }
                }
                requests.append(new_question)

            if requests:  # Proceed only if there are requests to add
                body = {'requests': requests}
                service.forms().batchUpdate(formId=form_id, body=body).execute()
                return f"https://docs.google.com/forms/d/{form_id}/edit"
            else:
                return {'error': 'Error payload', 'questions': questions}
        except HttpError as error:
            return {'error': str(error), 'error_details': error.error_details}


    @keyword("Add Questions And Answers From Google Doc To Form")
    def add_questions_and_answers_from_google_doc_to_form(self, doc_id, form_id):
        # Read content and answers from Google Doc
        questions, answer_keys = self.read_google_doc_content_and_answers(doc_id)
        
        
        # Check if there are no questions or answers to add
        if not questions:
            return {'error': 'No questions or answers parsed from the document', 'questions': questions, 'answers': answer_keys}

        # Map the correct answers to the questions
        for question in questions:
            question_num = str(question['title'].split()[1].replace(".", ""))
            if question_num in answer_keys:
                question['correct_answer'] = answer_keys[question_num]
            else:
                question['correct_answer'] = None
                
        return self.add_questions_to_form(form_id, questions)
