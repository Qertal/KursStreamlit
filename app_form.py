import streamlit as st

import pandas as pd

from memory_profiler import profile


@profile
def main():
    st.title("Streamlit forms & salary calculator")
    menu = ['Home','About']

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Forms tutorial")

        #salary calculator
        #combine forms + columns
        
        #docs

        # st.help(st.form)

        with st.form(key='salaryform', clear_on_submit=True):
            col1,col2,col3 = st.columns([3,2,1])

            with col1:
                amount = st.number_input("Hourly Rate in $")

            with col2:
                hour_per_week = st.number_input("Hours per week",1,120)
            
            with col3:
                st.text("Salary")
                submit_salary = st.form_submit_button(label='Calculate')
        
        if submit_salary:    
            with st.expander('Results'):
                daily = [amount * 8]
                weekly = [amount * hour_per_week]
                df = pd.DataFrame(
                    {
                        'hourly': amount,
                        'daily': daily,
                        'weekly': weekly
                        }
                        )
                st.dataframe(df.T,width=300)

        # Method 1: Context manager approach (with)
        with st.form(key='form1'):
            firstname = st.text_input("Firstname")
            lastname = st.text_input("Lastname")
            dob = st.date_input("Date of Birth")

            #important
            submit_button = st.form_submit_button(label='SignUp')

        #results can be either for or outside
        if submit_button:
            st.success(f"Hello {firstname}, you have created an account")


        #Method 2:
        form2 = st.form(key='form2')
        username = form2.text_input("Username")
        jobtype = form2.selectbox('Job',['Dev','Data scientist','Doctor'])
        submit_button2 = form2.form_submit_button("Login")

        if submit_button2:
            st.write(username.upper())


    else:
        st.subheader("About")

if __name__ == '__main__':
    main()