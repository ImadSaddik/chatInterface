<template>
    <section class="container vh-100 border-start border-end d-flex flex-column shadow">

        <div class="row p-2 border-bottom align-items-center">
            <div class="col">
                <i type="button" class="fs-4 bi bi-layout-sidebar" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample"></i>
                <SideBarVue @messages-received="(roomMessages) => loadRoom(roomMessages)"/>
            </div>
            <div class="col d-flex justify-content-center">
                <p class="fs-2 card-text">mimGPT</p>
            </div>
            <div class="col d-flex justify-content-end">
                <i v-if="theme === 'light'" type="button" class="fs-4 me-3 bi bi-brightness-high-fill" @click="toggleDarkMode"></i>
                <i v-else type="button" class="fs-4 me-3 bi bi-moon-stars-fill" @click="toggleDarkMode"></i>

                <i type="button" class="fs-4 me-3 bi bi-arrow-repeat" @click="clearRoom"></i>

                <i type="button" class="fs-4 bi bi-bookmarks" data-bs-toggle="modal" data-bs-target="#exampleModal"></i>
                <RoomModal :messages="messages"/>
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
                            v-if="obj.role === 'agent'"
                            :text="obj.message"
                            :speed="speed"
                            @animation-ended="(animationEnded) => this.canSendPrompt = animationEnded"
                        />

                        <p v-else class="card-text">{{ obj.message }}</p>
                    </div>

                </div>
            </div>
        </div>

        <div class="row p-2 border-top align-items-center">
            <div class="col">
                <textarea 
                    class="form-control resize-vertical rounded-4 shadow"
                    placeholder="Ask something ..."
                    @keydown.enter.prevent="sendPrompt"
                    style="resize: none;"
                    v-model="prompt"
                ></textarea>
            </div>

            <div class="col-auto">
                <i type="button" class="fs-4 bi bi-trash3" @click="prompt = null"></i>
            </div>
        </div>

    </section>
</template>
  
<script>
import axios from 'axios'
import TypeWritterEffect from './components/TypeWritterEffect.vue'
import RoomModal from './components/RoomModal.vue'
import SideBarVue from './components/SideBar.vue'

export default {
    name: 'App',
    components: {
        TypeWritterEffect,
        RoomModal,
        SideBarVue
    },
    data() {
        return {
            prompt: '',
            messages: [
                {
                    message: "Hey there, great to meet you. I’m Pi, your personal AI. My goal is to be useful, friendly and fun. Ask me for advice, for answers, or let’s talk about whatever’s on your mind. How's your day going?",
                    role: "agent" ,
                    position: "justify-content-start",
                    color: "bg-warning-subtle"
                }
            ],

            userPosition: "justify-content-end",
            agentPosition: "justify-content-start",
            
            userColor: "bg-info-subtle",
            agentColor: "bg-warning-subtle",
            
            speed: 10,
            canSendPrompt: true,
            currentTextIndex: 0,
            renderedTexts: [],

            theme: 'light'
        }
    },
    mounted() {
        this.speed = 0;
        this.showNextText();
    },
    methods: {
        async sendPrompt() {
            if (this.prompt === '' || !this.canSendPrompt) {
                return;
            }
            
            this.speed = 20;
            const messageObject = {
                message: this.prompt,
                role: "user" ,
                position: this.userPosition,
                color: this.userColor
            };
            this.addMessage(messageObject);
            const data = JSON.stringify({
                prompt: this.prompt
            })
            this.prompt = '';

            await axios
            .post('/api/v1/chat/', data, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': 'csrftoken'
                }
            })
            .then(response => {
                const messageObject = {
                    message: response.data.response,
                    role: "agent" ,
                    position: this.agentPosition,
                    color: this.agentColor
                };
                this.addMessage(messageObject);
            })
            .catch(error => {
                console.log(error)
                this.prompt = '';
            })

            
            this.showNextText();
        },
        addMessage(data) {
            this.messages.push(data);
            this.showNextText();
        },
        showNextText() {
            this.canSendPrompt = false;

            if (this.currentTextIndex < this.messages.length) {
                this.renderedTexts.push(this.messages[this.currentTextIndex]);
                this.currentTextIndex++;
            }
        },
        clearRoom() {
            console.log('clear room')
            this.messages = [];
            this.renderedTexts = [];
            this.currentTextIndex = 0;
        },
        loadRoom(roomMessages) {
            console.log('load room')
            this.messages = roomMessages;
            this.renderedTexts = [];
            this.speed = 0;

            for (let i = 0; i < this.messages.length; i++) {
                if (this.messages[i].role === 'agent') {
                    this.messages[i].position = this.agentPosition;
                    this.messages[i].color = this.agentColor;
                } else {
                    this.messages[i].position = this.userPosition;
                    this.messages[i].color = this.userColor;
                }

                this.renderedTexts.push(this.messages[i]);
            }

            this.currentTextIndex = this.messages.length;
        },
        toggleDarkMode() {
            const htmlElement = document.querySelector('html');
            const currentTheme = htmlElement.getAttribute('data-bs-theme');

            if (currentTheme === 'light') {
                htmlElement.setAttribute('data-bs-theme', 'dark');
                this.theme = 'dark';
            } else {
                htmlElement.setAttribute('data-bs-theme', 'light');
                this.theme = 'light';
            }

        }
    }
}
</script>
