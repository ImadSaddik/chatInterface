<template>
    <section class="container vh-100 border-start border-end d-flex flex-column shadow bg-light">

        <div class="row p-2 fs-4 border-bottom align-items-center">
            <div class="col">
                <i type="button" class="bi bi-layout-sidebar"></i>
            </div>
            <div class="col d-flex justify-content-center">
                <p class="fs-2 card-text">mimGPT</p>
            </div>
            <div class="col d-flex justify-content-end">
                <i type="button" class="bi bi-bookmarks"></i>
            </div>
        </div>

        <div class="row p-2 flex-grow-1 overflow-auto">
            <div class="flex-column">
                <div 
                    v-for="(obj, index) in renderedTexts" 
                    :key="index"
                    class="p-2 d-flex align-items-center"
                    :class="obj.position"
                >

                    <div class="p-2 rounded-3" :class="obj.color">
                        <TypeWritterEffect
                            :text="obj.message"
                            :speed="speed"
                            @animation-ended="(animationEnded) => this.disableButton = !animationEnded"
                        />
                    </div>

                </div>
            </div>
        </div>

        <div class="row p-2 border-top align-items-center">
            <div class="col">
                <textarea 
                    class="form-control resize-vertical rounded-4 bg-light shadow"
                    placeholder="Ask something ..."
                    @keyup.enter="sendPrompt"
                    style="resize: none;"
                    v-model="prompt"
                ></textarea>
            </div>

            <div class="col-auto">
                <i type="button" class="fs-4 bi bi-trash3" @click="prompt = ''"></i>
            </div>
        </div>

    </section>
</template>
  
<script>
import TypeWritterEffect from './components/TypeWritterEffect.vue'

export default {
    name: 'App',
    components: {
        TypeWritterEffect
    },
    data() {
        return {
            prompt: '',
            texts: [
                {
                    message: "Hey there, great to meet you. I’m Pi, your personal AI. My goal is to be useful, friendly and fun. Ask me for advice, for answers, or let’s talk about whatever’s on your mind. How's your day going?",
                    role: "agent" ,
                    position: "justify-content-start",
                    color: "bg-warning-subtle"
                },
                {
                    message: "What is django?",
                    role: "user" ,
                    position: "justify-content-end",
                    color: "bg-info-subtle"
                },
                {
                    message: "Django is a popular open-source web framework written in Python. It's used to build dynamic, data-driven websites and applications. The framework is lightweight and efficient, with a focus on reusability and rapid development. It also has a large ecosystem of third-party libraries and tools, making it a great choice for developing web applications. Have you used Django before?",
                    role: "agent" ,
                    position: "justify-content-start",
                    color: "bg-warning-subtle"
                },
                {
                    message: "How do I learn it",
                    role: "user" ,
                    position: "justify-content-end",
                    color: "bg-info-subtle"
                },
                {
                    message: "There are a lot of ways to learn Django. You can start by reading the Django documentation, which is a great resource for learning the basics. There are also many online tutorials and courses available, both free and paid. And if you prefer to learn by doing, you can try building a simple project with Django and learning as you go. There are also many online communities and forums where you can get help and support.",
                    role: "agent" ,
                    position: "justify-content-start",
                    color: "bg-warning-subtle"
                },
                {
                    message: "Can you point to me some good ressources?",
                    role: "user" ,
                    position: "justify-content-end",
                    color: "bg-info-subtle"
                },
                {
                    message: "Sure thing. A lot of people recommend starting with the Django documentation, which is a great resource for learning the basics. It covers everything from setting up a Django project to working with models and views. There are also many online tutorials and courses available, both free and paid. Some popular options include Udemy, Coursera, Pluralsight, and edX. These courses typically provide more in-depth instruction and hands-on practice than the documentation. They also often come with additional resources like quizzes, projects, and forums.",
                    role: "agent" ,
                    position: "justify-content-start",
                    color: "bg-warning-subtle"
                },
                {
                    message: "How  do I make a model in django?",
                    role: "user" ,
                    position: "justify-content-end",
                    color: "bg-info-subtle"
                },
                {
                    message: "Well, it's a bit of a process, but I'll walk you through it. To create a model in Django, you first need to create a new Python file that will contain your model definition. This file should be placed in the 'models' folder of your Django project. Then, you need to define a class that inherits from the 'Model' class provided by Django. This class will define the fields and properties of your model. For example, if you were creating a model for a blog post, you might have fields like 'title', 'author', and 'content'.",
                    role: "agent" ,
                    position: "justify-content-start",
                    color: "bg-warning-subtle"
                },
                {
                    message: "Thanks",
                    role: "user" ,
                    position: "justify-content-end",
                    color: "bg-info-subtle"
                }
            ],
            speed: 0,
            showButton: true,
            disableButton: false,
            currentTextIndex: 0,
            renderedTexts: []
        }
    },
    methods: {
        sendPrompt() {
            if (this.prompt.length > 0) {
                this.texts.push({
                    message: this.prompt,
                    role: "user" ,
                    position: "justify-content-end",
                    color: "bg-info-subtle"
                });
                this.prompt = '';
                this.showNextText();
            }
        },
        showNextText() {
            this.disableButton = true;

            if (this.currentTextIndex < this.texts.length) {
                this.renderedTexts.push(this.texts[this.currentTextIndex]);
                this.currentTextIndex++;
                this.showButton = this.currentTextIndex < this.texts.length;
            }
        }
    }
}
</script>
