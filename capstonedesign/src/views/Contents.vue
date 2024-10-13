<template>
    <TopNav/>
    <MainContainer>
      <div style="text-align: left;">
        <SubTitle>실시간 뉴스</SubTitle>
        <containerBox>
          <EconomyNews/>
        </containerBox>

        <SubTitle>맞춤 핫 토픽</SubTitle>
        <containerBox>
          <CustomHotTopic/>
        </containerBox>

      </div>
      <div style="text-align: left;">
        <SubTitle>교육 콘텐츠</SubTitle>
        <containerBox>
          <EducationContents/>
        </containerBox>

        <SubTitle>경제 상식 둘러보기</SubTitle>
        <containerBox>
          <EconomicInfo/>
        </containerBox>
      </div>
    </MainContainer>
    
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import containerBox from '../components/Box.vue'
  import SubTitle from '@/components/SubTitle.vue';
  import MainContainer from '@/components/MainContainer.vue';
  import EconomyNews from '@/components/ContentsPage/EconomyNews.vue';
  import CustomHotTopic from '@/components/ContentsPage/CustomHotTopic.vue';
  import EducationContents from '@/components/ContentsPage/EducationContents.vue';
  import EconomicInfo from '@/components/ContentsPage/EconomicInfo.vue';

  export default {
    name: 'ContentsPage',
    components: {
      TopNav,
      containerBox,
      SubTitle,
      MainContainer,
      EconomyNews,
      CustomHotTopic,
      EducationContents,
      EconomicInfo
    }
  }
  </script>
  
  <style>

  </style>
  