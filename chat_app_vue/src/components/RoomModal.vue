<template>
    <div class="modal fade" id="saveModal" tabindex="-1" aria-labelledby="saveModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="saveModalLabel">Save room</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="clearRoomName"></button>
            </div>
            <div class="modal-body">
                <div class="col-md">
                    <div class="form-floating">
                        <input type="text" class="form-control" id="floatingInput" placeholder="Room name" v-model="roomName">
                        <label for="floatingInput">Room name</label>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="clearRoomName">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="saveRoom">Save room</button>
            </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "RoomModal",
        props: ['messages'],
        data() {
            return {
                roomName: ''
            }
        },
        methods: {
            async saveRoom() {
                const data = JSON.stringify({
                    roomName: this.roomName,
                    messages: this.messages
                });

                await axios
                .post('/api/v1/saveRoom/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then((response) => {
                    console.log(response);
                    this.$emit('roomSaved');
                })
                .catch((error) => {
                    console.log(error);
                });
            },
            clearRoomName() {
                this.roomName = '';
            }
        }
    }
</script>