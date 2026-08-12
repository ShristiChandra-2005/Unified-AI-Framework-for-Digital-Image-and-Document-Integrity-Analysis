import hashlib
import hmac

import streamlit as st

from app import (
    ADMIN_DASHBOARD_PAGE,
    apply_theme,
    page_header,
    render_footer,
    render_sidebar,
)


ADMIN_USERNAME = "admin"
ADMIN_ROLE = "Administrator"

# Plain password is not stored in this file.
ADMIN_PASSWORD_HASH = (
    "f12deedb64f2a733d0a2a5293f42c1d33d21b27173ff1a2114e4b4d0b720693a"
)


def hash_password(password: str) -> str:
    """
    Convert entered password into SHA-256 hash.
    """

    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str) -> bool:
    """
    Compare entered password hash with stored password hash.
    """

    entered_hash = hash_password(password)

    return hmac.compare_digest(
        entered_hash,
        ADMIN_PASSWORD_HASH,
    )


def authenticate_admin(username: str, password: str) -> bool:
    """
    Validate admin username and password.
    """

    username_matches = hmac.compare_digest(
        username,
        ADMIN_USERNAME,
    )

    password_matches = verify_password(password)

    return username_matches and password_matches


def set_admin_session(username: str) -> None:
    """
    Store admin login state in Streamlit session.
    """

    st.session_state["is_admin"] = True
    st.session_state["admin_username"] = username
    st.session_state["admin_role"] = ADMIN_ROLE


def clear_admin_session() -> None:
    """
    Clear admin session during logout.
    """

    st.session_state.pop("is_admin", None)
    st.session_state.pop("admin_username", None)
    st.session_state.pop("admin_role", None)


def redirect_to_dashboard() -> None:
    """
    Redirect authenticated admin user to dashboard.
    """

    st.switch_page(ADMIN_DASHBOARD_PAGE)


apply_theme()
render_sidebar()

page_header(
    "Admin Login",
    (
        "Secure administrative access for reviewing report history, module usage, "
        "risk trends, generated evidence files, and analytics."
    ),
)

if st.session_state.get("is_admin"):
    st.success(
        f"Logged in as {st.session_state.get('admin_username', 'Admin')} "
        f"({st.session_state.get('admin_role', ADMIN_ROLE)})."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Open Admin Dashboard", width="stretch"):
            redirect_to_dashboard()

    with col2:
        if st.button("Logout", width="stretch"):
            clear_admin_session()
            st.rerun()

else:
    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown(
            """
            <div class="soft-card">
                <h3>Administrator Access</h3>
                <p>
                    The admin dashboard is protected so report history, risk analytics,
                    generated JSON files, and PDF evidence reports remain available only
                    after administrator login.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # st.info(
        #     "Admin login uses hashed password verification. "
        #     "The plain password is not stored in the source code."
        # )

    with right:
        st.markdown("### Sign In")

        with st.form("admin_login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button(
                "Login",
                width="stretch",
            )

        if submitted:
            cleaned_username = username.strip()

            if authenticate_admin(cleaned_username, password):
                set_admin_session(cleaned_username)
                st.success("Login successful. Redirecting to Admin Dashboard...")
                redirect_to_dashboard()
            else:
                st.error("Invalid username or password.")

render_footer()



