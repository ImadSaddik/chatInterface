<template>
    <div class="modal fade" id="editRoomModal" tabindex="-1" aria-labelledby="editRoomModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="editRoomModalLabel">Edit room</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="clearEditRoomName"></button>
            </div>
            <div class="modal-body">
                <div class="col-md">
                    <div class="form-floating">
                        <input type="text" class="form-control" id="floatingInput" placeholder="Room name" v-model="newRoomName">
                        <label for="floatingInput">Updated room name</label>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="clearEditRoomName">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editRoom">Save changes</button>
            </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    
    export default {
        name: "EditRoomModal",
        props: ['room'],
        data() {
            return {
                newRoomName: ''
            }
        },
        methods: {
            clearEditRoomName() {
                this.newRoomName = '';
            },
            async editRoom() {
                if (this.newRoomName === '') {
                    alert('Room name cannot be empty');
                    return;
                }

                const data = JSON.stringify({
                    newName: this.newRoomName,
                    id: this.room.id
                })

                await axios
                .post('/api/v1/editRoom/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    console.log(response);
                    this.$emit('roomEdited', response.data);
                })
                .catch(error => {
                    console.log(error);
                })

                this.newRoomName = '';
            }
        }
    }
</script>