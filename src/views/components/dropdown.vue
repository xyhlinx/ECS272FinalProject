<template>
    <div id="dropdown">
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
                selected: { id: 0, text: 'price' },
                types: [
                    { id: 0, type: 'price' },
                    { id: 1, type: 'metacritic_score' },
                    { id: 2, type: 'recommendations' },
                    { id: 3, type: 'achievements' }
                ]
            }
        },
        mounted(){
        },
        methods: {
            onChange(event) {
                console.log(this.selected.id, this.selected.text);
                this.$emit('selectedChange', this.selected);
            }
        }
    }
</script>