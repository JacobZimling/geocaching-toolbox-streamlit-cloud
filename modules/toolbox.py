from streamlit_float import *


def toolbox_header(page_header: str):
    st.set_page_config(layout="wide", page_title="PihlZimling's geocaching toolbox")
    # st.set_page_config("PihlZimling's geocaching toolbox")
    st.title("PihlZimling's geocaching toolbox")
    if len(page_header.strip()) > 0:
        st.header(page_header)

    # Float feature initialization
    float_init()

    # Initialize session variable that will show/hide Float Box
    if "show" not in st.session_state:
        st.session_state.show = False
    return


def toolbox_description():
    st.markdown("<p>Formålet med denne toolbox er at gøre livet som geocacher lidt nemmere. Til det formål har jeg udviklet nogle værktøjer, som jeg selv har savnet, både hjemme ved computeren og i marken, når der skal løses opgaver.</p>", unsafe_allow_html=True)
    st.markdown("<p>Menuen til venstre indeholder en liste med de tools der pt. er tilgængelige.</p>", unsafe_allow_html=True)
    st.markdown("<p>Er der noget der ikke virker eller har du et forslag til noget der kan gøre toolbox'en mere anvendelig, så brug feedback-knappen.</p>", unsafe_allow_html=True)
    return


def toolbox_feedback():
    # Container with expand/collapse button
    button_container = st.container()
    with button_container:
        if st.session_state.show:
            if st.button("⭳ Feedback", type="primary"):
                st.session_state.show = False
                st.rerun()
        else:
            if st.button("⭱ Feedback", type="secondary"):
                st.session_state.show = True
                st.rerun()

    # Alter CSS based on expand/collapse state
    if st.session_state.show:
        vid_y_pos = "2rem"
        button_b_pos = "12.5rem"
    else:
        vid_y_pos = "-19.5rem"
        button_b_pos = "1rem"

    button_css = float_css_helper(width="2.2rem", right="6rem", bottom=button_b_pos, transition=0)

    # Float button container
    button_container.float(button_css)

    # Add Float Box with feedback link
    float_box(
        "Er der noget der ikke virker eller har du et forslag til noget der kan gøre toolbox'en mere anvendelig? <a href='https://docs.google.com/forms/d/e/1FAIpQLSfOP2VDkTbB8yCI69zouOo7Z2VyHAmaUqc8RxdcHRUDkjBWuw/viewform'>Send din feedback her</a>",
        width="15rem", height="10rem", right="2rem", bottom=vid_y_pos,
        css="padding: 5;transition-property: all;transition-duration: .5s;transition-timing-function: cubic-bezier(0, 1, 0.5, 1);",
        shadow=12)
    return
