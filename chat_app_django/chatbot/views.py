import json
import random
import time

from django.http import JsonResponse

from rest_framework.decorators import api_view


responses = [
    "Artificial intelligence, often abbreviated as AI, refers to the simulation of human intelligence processes by machines. These processes include learning, reasoning, problem-solving, perception, and language understanding.",
    "Machine learning is a subset of AI that involves the development of algorithms allowing computers to learn from and make predictions or decisions based on data. It has applications in areas like image recognition, medical diagnosis, and financial forecasting.",
    "Deep learning, a specialized form of machine learning, utilizes neural networks with multiple layers to extract higher-level features from data. This has led to breakthroughs in tasks such as autonomous driving and natural language processing.",
    "Natural Language Processing (NLP) focuses on the interaction between computers and human language. NLP techniques enable machines to understand, interpret, and generate human language, which has led to advancements in chatbots, translation, and sentiment analysis.",
    "AI ethics is a growing field concerned with the responsible development and deployment of AI systems. This involves addressing biases in algorithms, ensuring transparency, and establishing guidelines for the ethical use of AI in various domains.",
    "Reinforcement learning is a learning paradigm where an agent learns by interacting with an environment and receiving feedback in the form of rewards or penalties. It has been used to train robots, optimize resource allocation, and develop strategies in games.",
    "AI-powered recommendation systems leverage user data to provide personalized suggestions. These systems are used in platforms like streaming services and e-commerce websites to enhance user experience and increase engagement.",
    "The potential of AI is immense, with applications spanning across industries such as healthcare, finance, manufacturing, and entertainment. As AI technology continues to advance, it is crucial to consider its societal impact and ensure its benefits are widely accessible.",
    "Quantum computing is an area that holds promise for AI advancement. Quantum AI aims to harness the power of quantum computers to solve complex problems more efficiently, potentially revolutionizing fields like cryptography and optimization.",
    "AI in healthcare has the potential to transform patient care. From disease diagnosis to personalized treatment recommendations, AI-driven tools can analyze large datasets and assist medical professionals in making more accurate decisions.",
    "Chatbots are a common application of AI that simulates human conversation. They are used for customer support, information retrieval, and even as virtual companions, demonstrating the progress made in natural language understanding."
  ]


@api_view(['POST'])
def chat(request):
    global responses
    prompt = json.loads(request.body)['prompt']
    # if we have access to a pretrained model, we can feed the prompt into the model and get a response
    
    response = responses[random.randint(0, len(responses) - 1)]
    
    return JsonResponse({'response': response})