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
                            <div class="group d-flex flex-row align-items-center mb-2" v-for="(room, index) in rooms" :key="index">
                                <button
                                    class="list-group-item list-group-item-action rounded-2"
                                    aria-current="true"
                                    :class="{ active: selectedRoomIndex === index }"
                                    @click="selectRoom(index)"
                                >
                                    {{ room.name }}
                                </button>
                                <i type="button" class="fs-5 mx-3 bi bi-pencil-square" data-bs-toggle="modal" data-bs-target="#editRoomModal" @click="this.selectedRoomIndex = index"></i>
                                <i type="button" class="fs-5 m bi bi-trash3" @click="deleteRoom(index)"></i>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <EditRoomModal :room="this.rooms[this.selectedRoomIndex]" @room-edited="this.getRooms()"/>
</template>

<script>
    import axios from 'axios';
    import EditRoomModal from './EditRoomModal.vue';

    export default {
        name: 'SideBar',
        components: {
            EditRoomModal
        },
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
            },
            async deleteRoom(index) {
                const data = {
                    id: this.rooms[index].id
                };
                
                await axios
                .post('/api/v1/deleteRoom/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    console.log(response.data);
                    this.getRooms();
                })
                .catch(error => {
                    console.log(error);
                });
            }
        }
    }
</script>
