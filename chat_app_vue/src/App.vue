<template>
  <section
    class="container vh-100 border-start border-end d-flex flex-column shadow"
  >
    <div class="row p-2 border-bottom align-items-center">
      <div class="col-2">
        <i
          type="button"
          class="fa-solid fa-expand fa-lg me-3"
          data-bs-toggle="offcanvas"
          data-bs-target="#offcanvasExample"
          aria-controls="offcanvasExample"
        ></i>
        <SideBarVue
          ref="sidebar"
          :messages="messages"
          @messages-received="(roomMessages) => loadRoom(roomMessages)"
        />

        <i
          v-if="theme === 'light'"
          type="button"
          class="fa-solid fa-sun fa-lg me-3"
          @click="toggleDarkMode"
        ></i>
        <i
          v-else
          type="button"
          class="fa-solid fa-moon fa-lg me-3"
          @click="toggleDarkMode"
        ></i>

        <i
          type="button"
          class="fa-solid fa-arrow-rotate-right fa-lg me-3"
          @click="clearRoom"
        ></i>

        <i
          type="button"
          class="fa-solid fa-floppy-disk fa-lg"
          data-bs-toggle="modal"
          data-bs-target="#saveModal"
        ></i>
        <RoomModal
          :messages="messages"
          @room-saved="this.$refs.sidebar.getRooms()"
        />
      </div>
      <div class="col-8 d-flex justify-content-center">
        <p class="fs-2 card-text">ChatG2IA</p>
      </div>
      <div class="col-2 p-0">
        <div>
          <div
            class="dropdown"
            :class="
              theme === 'light' ? 'light-mode-dropdown' : 'dark-mode-dropdown'
            "
          >
            <button
              class="btn btn-secondary dropdown-toggle w-100"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ selectedModel }}
            </button>
            <ul class="dropdown-menu w-100">
              <li>
                <a class="dropdown-item" @click="selectedModel = model1">{{
                  model1
                }}</a>
              </li>
              <li>
                <a class="dropdown-item" @click="selectedModel = model2">{{
                  model2
                }}</a>
              </li>
              <li>
                <a class="dropdown-item" @click="selectedModel = model3">{{
                  model3
                }}</a>
              </li>
              <li>
                <a class="dropdown-item" @click="selectedModel = model4">{{
                  model4
                }}</a>
              </li>
            </ul>
          </div>
        </div>
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
              @animation-ended="
                (animationEnded) => (this.canSendPrompt = animationEnded)
              "
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
          style="resize: none"
          v-model="prompt"
        ></textarea>
      </div>

      <div class="col-auto">
        <i
          type="button"
          class="fa-solid fa-trash fa-lg"
          @click="prompt = null"
        ></i>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import TypeWritterEffect from "./components/TypeWritterEffect.vue";
import RoomModal from "./components/RoomModal.vue";
import SideBarVue from "./components/SideBar.vue";

export default {
  name: "App",
  components: {
    TypeWritterEffect,
    RoomModal,
    SideBarVue,
  },
  data() {
    return {
      prompt: "",
      messages: [],
      defaultMessage: {
        message:
          "Hey there, great to meet you. I am your personal AI. My goal is to be useful, friendly and fun. Ask me for advice, for answers, or let us talk about whatever is on your mind. How's your day going?",
        role: "agent",
        position: "justify-content-start",
        color: "bg-warning-subtle",
      },

      userPosition: "justify-content-end",
      agentPosition: "justify-content-start",

      userColor: "bg-info-subtle",
      agentColor: "bg-warning-subtle",

      speed: 10,
      canSendPrompt: true,
      currentTextIndex: 0,
      renderedTexts: [],

      theme: "light",

      selectedModel: "mistral-7b-instruct",
      model1: "mistral-7b-instruct",
      model2: "llama-2-13b-chat",
      model3: "falcon-7b-instruct",
      model4: "vicuna-8b-instruct",
    };
  },
  mounted() {
    this.speed = 0;
    this.messages.push(this.defaultMessage);
    this.showNextText();
  },
  methods: {
    async sendPrompt() {
      if (this.prompt === "" || !this.canSendPrompt) {
        return;
      }

      this.speed = 20;
      const messageObject = {
        message: this.prompt,
        role: "user",
        position: this.userPosition,
        color: this.userColor,
      };
      this.addMessage(messageObject);
      const data = JSON.stringify({
        prompt: this.prompt,
        model: this.selectedModel,
      });
      this.prompt = "";

      await axios
        .post("/api/v1/chat/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          const messageObject = {
            message: response.data.response,
            role: "agent",
            position: this.agentPosition,
            color: this.agentColor,
          };
          this.addMessage(messageObject);
        })
        .catch((error) => {
          console.log(error);
          this.prompt = "";
        });

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
      this.canSendPrompt = true;
      this.$refs.sidebar.selectedRoomIndex = -1;

      this.messages = [this.defaultMessage];
      this.renderedTexts = [this.defaultMessage];
      this.currentTextIndex = this.messages.length;
    },
    loadRoom(roomMessages) {
      this.messages = roomMessages;
      this.renderedTexts = [];
      this.speed = 0;

      for (let i = 0; i < this.messages.length; i++) {
        if (this.messages[i].role === "agent") {
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
      const htmlElement = document.querySelector("html");
      const currentTheme = htmlElement.getAttribute("data-bs-theme");

      if (currentTheme === "light") {
        htmlElement.setAttribute("data-bs-theme", "dark");
        this.theme = "dark";
      } else {
        htmlElement.setAttribute("data-bs-theme", "light");
        this.theme = "light";
      }
    },
  },
};
</script>

<style>
.light-mode-dropdown {
  background-color: white;
}

.light-mode-dropdown .dropdown-toggle {
  background-color: white;
  border: 1px solid #333;
  color: #333;
}

.light-mode-dropdown .dropdown-item {
  color: #333;
}

.dark-mode-dropdown {
  background-color: #333;
}

.dark-mode-dropdown .dropdown-toggle {
  background-color: #333;
  border: 1px solid #495057;
  color: white;
}

.dark-mode-dropdown .dropdown-item {
  color: white;
}

.btn.dropdown-toggle {
  text-align: left;
  padding-right: 2rem;
  position: relative;
}

.btn.dropdown-toggle::after {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: 10px;
}
</style>
