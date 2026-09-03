import streamlit as st
from datetime import datetime #pip install streamlit-datetime-picker
import pandas as pd #pip install pandas
from supabase import create_client, Client #pip install streamlit supabase

# Supabase 연결
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

st.subheader("🚍 동원훈련 탑승정보 조회")
st.divider()
name = st.text_input("이름", max_chars=4)
phone = st.text_input("전화번호 뒷자리 (4자리)", max_chars=4)
if st.button("버스정보 조회하기"):
    if not name or not phone:
        st.error("이름과 전화번호 뒷자리를 모두 입력해주세요.")
    elif not phone.isdigit():
        st.error("전화번호 뒷자리는 숫자만 입력 가능합니다.")
    elif len(name) < 2:
        st.error("이름은 두글자 이상 입력해주세요")
    elif len(phone) != 4:
        st.error("전화번호 뒷자리는 4자리로 입력해주세요.")
    else:
        phone3=phone[-3:]
        
        if len(name) >= 3:
            first_char = name[0]
            third_char = name[2]

            res = (supabase.table("businfo")
              .select("*")
               .like("name", f"{first_char}_{third_char}")
               .eq("phone", phone3)
               .execute())
        elif len(name) == 2:
            first_char = name[0]
            third_char = "O"
            res = (supabase.table("businfo")
              .select("*")
               .like("name", f"{first_char}{third_char}")
               .eq("phone", phone3)
               .execute())
        else:
            print("이름을 다시 입력해주세요")

        if not res.data:
            st.warning("일치하는 정보가 없습니다.")
        elif len(res.data) > 1:
            st.error("중복 데이터가 있습니다. 직원에게 문의하세요.")
        else:
            busno = res.data[0]["busno"]
            st.markdown(
                f"""
                <div style='background-color:#d4edda; padding:15px; border-radius:10px;'>
                    <span style='font-size:16px; color:#155724;'>
                        {name}님께서 승차하실 버스번호는
                    </span><br>
                    <span style='font-size:35px; font-weight:bold; color:#0b5394;'>
                        {busno} 호차
                    </span>
                    <span style='font-size:16px; color:#155724;'>
                        입니다.
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
notice = """
📢 **공지사항**  
- 본 서비스는 동원훈련 탑승버스 조회 전용입니다.  
- 개인정보 보호를 위해 불필요한 정보는 저장하지 않으며, 모든 내용은 익명으로 처리됩니다.
- 문제가 발생하면 직원에게 문의하세요.  
"""
st.divider()
st.markdown(notice)

    
