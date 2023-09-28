# mimChat

## Description
mimChat is a `python/vue` project that aims to create a simple chat interface. In the backend we use django and you can put there any pretrain model to receive the response and get it displayed in the interface. mim by the way stands for `Made in Morocco`

## Key Features
- Easy to use.
- The ability to save, edit, and delete rooms.
- The possibility of using your own model in the backend.

## Getting Started
To get started with this project, follow these steps:

1. Clone the repository: `git clone https://github.com/ImadSaddik/chatInterface.git`
2. Install the required dependencies: `pip install -r requirements.txt`, the file is inside `chat_app_django`
3. Go to `chat_app_vue` and run: `npm install`
4. Go to `chat_app_django` and run: `python manage.py migrate` & `python manage.py runserver`
5. Go to `chat_app_vue` and run: `npm run serve`


## Use your own model
You need to go to the file located in `chat_app_django/chatbot/views.py` and import your model there. After importing the model delete this line of code `response = responses[random.randint(0, len(responses) - 1)]` and use your model instead to get the response.

```python
@api_view(['POST'])
def chat(request):
  global responses
  prompt = json.loads(request.body)['prompt']
  # if we have access to a pretrained model, we can feed the prompt into the model and get a response
  
  response = responses[random.randint(0, len(responses) - 1)]
  
  return JsonResponse({'response': response})
```
