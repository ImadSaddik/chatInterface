<template>
    <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasExampleLabel">Rooms</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <div>
                <div class="row">
                    <div class="col">
                        <div class="list-group">
                            <button
                                class="list-group-item list-group-item-action"
                                aria-current="true"
                                v-for="(room, index) in rooms"
                                :key="index"
                                :class="{ active: selectedRoomIndex === index }"
                                @click="selectRoom(index)"
                            >
                                {{ room.name }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'SideBar',
        data() {
            return {
                rooms: [],
                selectedRoomIndex: -1
            }
        },
        mounted() {
            this.getRooms();
        },
        methods: {
            async getRooms() {
                await axios
                .get('/api/v1/getRooms/')
                .then(response => {
                    this.rooms = response.data;
                })
                .catch(error => {
                    console.log(error);
                });
            },
            async selectRoom(index) {
                this.selectedRoomIndex = index;
                const data = {
                    id: this.rooms[index].id
                };
                
                await axios
                .get('/api/v1/getRoomMessages/', {
                    params: data,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    console.log(response.data);
                    this.$emit('messagesReceived', response.data);
                })
                .catch(error => {
                    console.log(error);
                });
            }
        }
    }
</script>
