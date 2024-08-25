from stpyvista.utils import start_xvfb

if "IS_XVFB_RUNNING" not in st.session_state:
  start_xvfb()
  st.session_state.IS_XVFB_RUNNING = True 
