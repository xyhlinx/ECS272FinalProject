<template>
    <div id="dropdown2">
        <select v-model="selected" @change="onChange($event)" class="form-control">
            <option v-for="p in types" v-bind:value="{ id: p.id, text: p.type }">{{p.type}}
            </option>
        </select>
    </div>
</template>

<script>
    import * as d3 from "d3";
    
    export default {
        name: 'Dropdown',
        data() {
            return {
                selected: { id: 0, text: 'genres' },
                types: [
                    { id: 0, type: 'genres' },
                    { id: 1, type: 'price_tag' },
                    { id: 2, type: 'estimated_owners' }
                ]
            }
        },
        mounted(){
        },
        methods: {
            onChange(event) {
                console.log(this.selected.id, this.selected.text);
                this.$emit('home_selection', this.selected);
            }
        }
    }
</script>