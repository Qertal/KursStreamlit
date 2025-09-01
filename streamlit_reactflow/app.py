# import streamlit as st

# from streamlit_flow import streamlit_flow
# from streamlit_flow.elements import StreamlitFlowEdge, StreamlitFlowNode
# from streamlit_flow.layouts import TreeLayout
# from streamlit_flow.state import StreamlitFlowState

# def home_page():
#     st.subheader("Home Page")

#     nodes = [
#         StreamlitFlowNode(id='1', pos=(0, 0), data={'content': 'Node 1'}, node_type='input', source_position='right'),
#         StreamlitFlowNode('2', (0, 0), {'content': 'Node 2'}, 'default', 'right', 'left'),
#         StreamlitFlowNode('3', (0, 0), {'content': 'Node 3'}, 'default', 'right', 'left'),
#         StreamlitFlowNode('4', (0, 0), {'content': 'Node 4'}, 'output', 'right', 'left'),
#         StreamlitFlowNode('5', (0, 0), {'content': 'Node 5'}, 'output', 'right', 'left'),
#         StreamlitFlowNode('6', (0, 0), {'content': 'Node 6'}, 'output', 'right', 'left'),
#         StreamlitFlowNode('7', (0, 0), {'content': 'Node 7'}, 'output', 'right', 'left'),
#     ]

#     edges = [
#         StreamlitFlowEdge('1-2', '1', '2', animated=True),
#         StreamlitFlowEdge('1-3', '1', '3', animated=True),
#         StreamlitFlowEdge('2-4', '2', '4', animated=True),
#         StreamlitFlowEdge('2-5', '2', '5', animated=True),
#         StreamlitFlowEdge('3-6', '3', '6', animated=True),
#         StreamlitFlowEdge('3-7', '3', '7', animated=True),
#     ]

#     state = StreamlitFlowState(nodes, edges)

#     streamlit_flow("tree_layout", state, layout=TreeLayout(direction='right'), fit_view=True)

# def about_page():
#     st.subheader("About Page")


# PAGES = {
#     "Home": home_page,
#     "About": about_page,
# }

# selection = st.sidebar.radio("Page", list(PAGES.keys()))
# page = PAGES[selection]
# page()

# import streamlit as st
# from streamlit_flow import streamlit_flow
# from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
# from streamlit_flow.state import StreamlitFlowState

# nodes = [StreamlitFlowNode('1', (100, 100), {'content': 'Green Node'}, 'input', 'right', draggable=False, style={'color': 'white', 'backgroundColor': '#00c04b', 'border': '2px solid white'}),
# 	StreamlitFlowNode('2', (350, 25), {'content': 'Smol Node'}, 'output', 'right', 'left', draggable=False, style={'fontSize': '8px', 'padding': 0, 'width': '40px'}),
# 	StreamlitFlowNode('3', (350, 175), {'content': 'Regular Node'}, 'output', 'right', 'left', draggable=False)]

# edges = [StreamlitFlowEdge('1-2', '1', '2', animated=True, label="edge", label_show_bg=True, label_bg_style={'stroke': 'red', 'fill': 'gray'}),
# 	StreamlitFlowEdge('1-3', '1', '3', animated=True)]

# if 'custom_styles_state' not in st.session_state:	
# 	st.session_state.custom_styles_state = StreamlitFlowState(nodes, edges)

# streamlit_flow('custom_style_flow',
# 		st.session_state.custom_styles_state,
# 		fit_view=True,
# 		show_minimap=False,
# 		show_controls=False,
# 		pan_on_drag=False,
# 		allow_zoom=False)

import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge 
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import LayeredLayout
        
nodes = [
    StreamlitFlowNode(id='1', pos=(0, 200), data={'content': 'Wejście na stronę\nBiPoint'}, node_type='input', source_position='right', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('2', (200, 200), {'content': 'Przekierowanie do\nKeyCloaka'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('3', (350, 120), {'content': 'Logowanie\nza pomocą credentiali'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('4', (350, 280), {'content': 'Czy konto bipoint\njuż istnieje?'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    # these four nodes are forced to the same x to form a single column on the right
    StreamlitFlowNode('5', (700, 80), {'content': 'Przekierowanie na pointa\ni tworzenie konta'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('6', (700, 220), {'content': 'Przekierowanie do pointa\ni zalogowanie'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('7', (200, 60), {'content': 'Logowanie za pomocą SSO\n(przekierowanie na okte)'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('8', (350, 60), {'content': 'Logowanie\ndo okty'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('10', (500, 60), {'content': 'Czy konto KeyCloak/\nBiPoint istnieje?'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('11', (500, 160), {'content': 'Przekierowanie na KeyCloak\ni przesłanie claimów'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('12', (500, 260), {'content': 'Utworzenie konta KeyCloak,\nuzupełnienie danych za pomocą claimów'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('13', (700, 360), {'content': 'Przekierowanie na BiPoint\ni tworzenie konta'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('14', (500, 360), {'content': 'Synchronizacja z\nkontem keycloak'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('15', (700, 500), {'content': 'Przekierowanie do BiPoint\ni zalogowanie'}, 'default', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
    StreamlitFlowNode('16', (900, 300), {'content': 'Witamy w BiPoint!\n:D'}, 'output', 'right', 'left', style={'whiteSpace': 'pre-wrap'}),
]

edges = [
    StreamlitFlowEdge('1-2', '1', '2', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('2-3', '2', '3', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('3-4', '3', '4', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('4-5', '4', '5', animated=True, label="Nie", label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('5-16', '5', '16', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('4-6', '4', '6', animated=True, label="Tak", label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('6-16', '6', '16', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('2-7', '2', '7', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('7-8', '7', '8', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('8-10', '8', '10', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('10-11', '10', '11', animated=True, label='Nie', label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('11-12', '11', '12', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('12-13', '12', '13', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('13-16', '13', '16', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('10-14', '10', '14', animated=True, label='Tak', label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('14-15', '14', '15', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
    StreamlitFlowEdge('15-16', '15', '16', animated=True, label_show_bg=True, label_bg_style={'stroke': 'black', 'fill': 'white'}),
]

if 'flow_state' not in st.session_state:
    st.session_state.flow_state = StreamlitFlowState(nodes, edges)
# Make the page use the full width and attempt to fill viewport height.
st.set_page_config(layout='wide')

# Inject CSS to reduce paddings and make main area fill the viewport height so
# the flow component can occupy the full page.
st.markdown(
    """<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main, .block-container {
        height: 100vh;
        margin: 0;
        padding: 0;
    }
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    .stApp { overflow: hidden; }
    /* Make common React Flow / component wrappers fill the viewport height */
    .reactflow-wrapper, .react-flow, .react-flow__viewport, .react-flow__renderer, .streamlit-flow, iframe {
        height: 100vh !important;
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render the flow (fit_view=True helps to center/fit nodes in view)
streamlit_flow('tree_layout', st.session_state.flow_state, layout=LayeredLayout(direction='right'), fit_view=True) 