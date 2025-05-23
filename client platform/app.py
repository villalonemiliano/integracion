import streamlit as st

def login():
    st.title("Welcome!")
    c1,c2 = st.columns(2)
    with c1:
        st.image("assets/bill.png")
    with c2:
        st.empty()
    st.header("Inicio de sesión")
    if st.button("Log in"):
        st.login("auth0")

def logout():
    st.title("Cerrar sesión")
    if st.button("Log out"):
        st.logout()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "reports/dashboard.py", title="Inicio", default=True
)
bugs = st.Page("reports/bugs.py", title="Ventajas Competitivas")
alerts = st.Page(
    "reports/alerts.py", title="Algoritmo"
)

search = st.Page("tools/search.py", title="Tu API")
history = st.Page("tools/history.py", title="Comentarios")

if st.experimental_user.is_logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
