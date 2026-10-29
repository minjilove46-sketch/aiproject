
import streamlit as st
st. title('이다인 이리와')
a=st.text_input('이다인의 단점을 써주세요')
b=st.selectcobox('이다인의 단점을 선택하세요',['멘헤라다','김민준을 좋아한다','조용하다'])
if st.button('저는 이다인입니다'):
  st.write('당신도 다인이가 멍청하다고 생각하시는군요!')
  st.info(a+'다인님! 안녕하세욧!')
  st.warning(b+'다인이를 좋아하시네요!')
  st.error('잘 부탁드립니다!')
  st.balloons()
