<template>
    <Box class="newsBox">
        <img src="https://placehold.co/600x600" class="thumbnail"/>
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <div class="newsTitle">
                뉴스 제목
            </div>
            <div class="company">
                언론사
            </div>
        </div>
        
    </Box>
</template>
<script>
import Box from '../Box.vue';
export default {
    components:{
        Box
    }
}
</script>
<style>

    .newsBox{
        width: 93%;
        display: flex;
    }

    .newsTitle{
        font-size: 20px;
        margin-bottom: 10px;
    }

    .thumbnail{
        width: 50px;
        height: 50px;
    }
</style>