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

# Page config must be set before any other Streamlit calls
# Start with sidebar collapsed and remove interactive sidebar controls so
# the app always behaves as if the fullscreen checkbox were unchecked.
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# Legend explaining node colors / roles
st.markdown(
        """
        <div style="display:flex; gap:1rem; align-items:center; margin-bottom:1rem;">
            <div style="display:flex; gap:.5rem; align-items:center;">
                <div style="width:18px; height:18px; background:#007acc; border-radius:3px; border:1px solid #ccc"></div>
                <div><strong>SP</strong> — BiPoint (Service Provider)</div>
            </div>
            <div style="display:flex; gap:.5rem; align-items:center;">
                <div style="width:18px; height:18px; background:#ff8c00; border-radius:3px; border:1px solid #ccc"></div>
                <div><strong>Keycloak</strong> — IdP / SP-broker</div>
            </div>
            <div style="display:flex; gap:.5rem; align-items:center;">
                <div style="width:18px; height:18px; background:#2ecc71; border-radius:3px; border:1px solid #ccc"></div>
                <div><strong>Okta</strong> — IdP</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

# Define nodes using explicit keyword args to avoid positional-arg mistakes
nodes = [
    StreamlitFlowNode(id='1', pos=(0, 200), data={'content': '[BiPoint] Wejście na stronę\nBiPoint'}, node_type='input', source_position='right', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
    StreamlitFlowNode(id='2', pos=(200, 200), data={'content': '[Keycloak]\nPrzekierowanie do\nKeyCloaka'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#ff8c00', 'border': '2px solid white'}),
    StreamlitFlowNode(id='3', pos=(350, 120), data={'content': '[Keycloak]\nLogowanie\nza pomocą credentiali'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#ff8c00', 'border': '2px solid white'}),
    StreamlitFlowNode(id='4', pos=(350, 280), data={'content': '[BiPoint]\nCzy konto bipoint\njuż istnieje?'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
    # these four nodes are forced to the same x to form a single column on the right
    StreamlitFlowNode(id='5', pos=(700, 80), data={'content': '[BiPoint] Przekierowanie na pointa\ni tworzenie konta'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
    StreamlitFlowNode(id='6', pos=(700, 220), data={'content': '[BiPoint] Przekierowanie do pointa\ni zalogowanie'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
    StreamlitFlowNode(id='7', pos=(200, 60), data={'content': '[Okta]\nLogowanie za pomocą SSO\n(przekierowanie na okte)'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#2ecc71', 'border': '2px solid white'}),
    StreamlitFlowNode(id='8', pos=(350, 60), data={'content': '[Okta]\nLogowanie\ndo okty'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#2ecc71', 'border': '2px solid white'}),
    StreamlitFlowNode(id='10', pos=(500, 60), data={'content': '[Keycloak]\nCzy konto KeyCloak/\nBiPoint istnieje?'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#ff8c00', 'border': '2px solid white'}),
    StreamlitFlowNode(id='11', pos=(500, 160), data={'content': '[Keycloak]\nPrzekierowanie na KeyCloak\ni przesłanie claimów'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#ff8c00', 'border': '2px solid white'}),
    StreamlitFlowNode(id='12', pos=(500, 260), data={'content': '[Keycloak]\nUtworzenie konta KeyCloak,\nuzupełnienie danych za pomocą claimów'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#ff8c00', 'border': '2px solid white'}),
    StreamlitFlowNode(id='13', pos=(700, 360), data={'content': '[BiPoint] Przekierowanie na BiPoint\ni tworzenie konta'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
    StreamlitFlowNode(id='14', pos=(500, 360), data={'content': '[Keycloak]\nSynchronizacja z\nkontem keycloak'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#ff8c00', 'border': '2px solid white'}),
    StreamlitFlowNode(id='15', pos=(700, 500), data={'content': '[BiPoint] Przekierowanie do BiPoint\ni zalogowanie'}, node_type='default', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
    StreamlitFlowNode(id='16', pos=(900, 300), data={'content': '[BiPoint] Witamy w BiPoint!\n:D'}, node_type='output', source_position='right', target_position='left', style={'whiteSpace': 'pre-wrap', 'color': 'white', 'backgroundColor': '#007acc', 'border': '2px solid white'}),
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

# Sidebar removed; no fullscreen CSS is injected so the view behaves like the
# checkbox would be unchecked (normal, non-fullscreen layout).

# Render the flow (fit_view=True helps to center/fit nodes in view)
streamlit_flow('tree_layout', st.session_state.flow_state, layout=LayeredLayout(direction='right'), fit_view=True)