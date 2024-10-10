<template>
    <TopNav/>

    <SearchBar/>
    <div style="margin-left: 10px;">
      <ButtonContainer>
        <SmallButton>
          국내
        </SmallButton>
        <SmallButton>
          해외
        </SmallButton>
      </ButtonContainer>
      <ButtonContainer>
        <SmallButton>
          전체
        </SmallButton>
        <SmallButton>
          성장 기대주
        </SmallButton>
        <SmallButton>
          안정 성장주
        </SmallButton>
        <SmallButton>
          고수익 저평가
        </SmallButton>
        <SmallButton>
          저평가 성장주
        </SmallButton>
      </ButtonContainer>
      <div style="display: flex; justify-content: space-between; margin-right: 10px;">
        <ButtonContainer>
          <select>
            <option value="1">조건 추가</option>
          </select>
          <SmallButton>
            카테고리
          </SmallButton>
          <SmallButton>
            시가총액
          </SmallButton>
        </ButtonContainer>

        <ButtonContainer>
          <SmallButton>
            관련 핫토픽
          </SmallButton>
          <SmallButton>
            전문가 의견
          </SmallButton>
          <SmallButton>
            비슷한 종목
          </SmallButton>
        </ButtonContainer>
      </div>
    </div>
    <ScrollContainer>
      <table>
        <tr>
          <th scope="col">종목</th>
          <th scope="col"></th>
          <th scope="col">현재가</th>
          <th scope="col">거래량</th>
          <th scope="col">시가총액</th>
          <th scope="col"></th>
        </tr>
        <tr>
          <td>삼성전자</td>
          <td></td>
          <td>60600</td>
          <td>23,107,725</td>
          <td>361조 7688억</td>
          <td></td>
        </tr>
      </table>
    </ScrollContainer>
    
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import SearchBar from '@/components/DetailPage/Search.vue';  
  import SmallButton from '@/components/SmallButton.vue';
  import ButtonContainer from '@/components/ButtonContainer.vue';
  import ScrollContainer from '@/components/ScrollContainer.vue';

  export default {
    name: 'DetailPage',
    components: {
      TopNav,
      SearchBar,
      SmallButton,
      ButtonContainer,
      ScrollContainer
    }
  }
  </script>
  
  <style>

  </style>
  