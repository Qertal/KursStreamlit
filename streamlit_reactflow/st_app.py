import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowEdge, StreamlitFlowNode
from streamlit_flow.layouts import TreeLayout
from streamlit_flow.state import StreamlitFlowState

def home_page():
    st.subheader("Home Page")

    nodes = [
        StreamlitFlowNode(id='1', pos=(0, 0), data={'content': 'Node 1'}, node_type='input', source_position='right'),
        StreamlitFlowNode('2', (0, 0), {'content': 'Node 2'}, 'default', 'right', 'left'),
        StreamlitFlowNode('3', (0, 0), {'content': 'Node 3'}, 'default', 'right', 'left'),
        StreamlitFlowNode('4', (0, 0), {'content': 'Node 4'}, 'output', target_position='left'),
        StreamlitFlowNode('5', (0, 0), {'content': 'Node 5'}, 'output', target_position='left'),
        StreamlitFlowNode('6', (0, 0), {'content': 'Node 6'}, 'output', target_position='left'),
        StreamlitFlowNode('7', (0, 0), {'content': 'Node 7'}, 'output', target_position='left'),
    ]

    edges = [
        StreamlitFlowEdge('1-2', '1', '2', animated=True),
        StreamlitFlowEdge('1-3', '1', '3', animated=True),
        StreamlitFlowEdge('2-4', '2', '4', animated=True),
        StreamlitFlowEdge('2-5', '2', '5', animated=True),
        StreamlitFlowEdge('3-6', '3', '6', animated=True),
        StreamlitFlowEdge('3-7', '3', '7', animated=True),
    ]

    state = StreamlitFlowState(nodes, edges)

    streamlit_flow("tree_layout", state, layout=TreeLayout(direction='right'), allow_new_edges=True, enable_pane_menu=True, enable_edge_menu=True,enable_node_menu=True)

def about_page():
    st.subheader("About Page")
    st.write("To jest strona o aplikacji.")

home = st.Page(home_page, title="Home")
about = st.Page(about_page, title="About")


pg = st.navigation({
    "Home":[home],
    "About": [about]
})

pg.run()