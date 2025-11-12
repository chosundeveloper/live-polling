#!/usr/bin/env python3
"""
AI Frontend Dream Team - LangGraph Multi-Agent
무료 최강 조합: Gemini + Groq + Mistral + Codex
"""

import os
import sys
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

load_dotenv()
console = Console()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not any([GOOGLE_API_KEY, GROQ_API_KEY, MISTRAL_API_KEY, OPENAI_API_KEY]):
    console.print("[red]❌ Error: No API keys found[/red]")
    sys.exit(1)

# Initialize AI models
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
) if GOOGLE_API_KEY else None

groq_qwen = ChatGroq(
    model="qwen2.5-coder-32k:latest",  # HTML/CSS 전문
    groq_api_key=GROQ_API_KEY,
    temperature=0.5
) if GROQ_API_KEY else None

groq_llama = ChatGroq(
    model="llama-3.3-70b-versatile",  # JS 로직
    groq_api_key=GROQ_API_KEY,
    temperature=0.7
) if GROQ_API_KEY else None

mistral = ChatMistralAI(
    model="codestral-latest",  # 애니메이션 전문
    mistral_api_key=MISTRAL_API_KEY,
    temperature=0.6
) if MISTRAL_API_KEY else None

codex = ChatOpenAI(
    model="gpt-4o-mini",  # 통합 및 품질 점검
    api_key=OPENAI_API_KEY,
    temperature=0.4
) if OPENAI_API_KEY else None

# State
class FrontendState(TypedDict):
    task: str
    design_concept: str
    html_css: str
    animations: str
    javascript: str
    ux_review: str
    final_code: str

# Agents
def visual_designer(state: FrontendState):
    """Gemini - 디자인 컨셉"""
    console.print("[cyan]🎨 Visual Designer (Gemini) designing concept...[/cyan]")

    llm = gemini or groq_llama
    messages = [
        SystemMessage(content="""You are an award-winning UI/UX designer. Create:
        1. Design concept and mood
        2. Color palette (hex codes)
        3. Typography choices
        4. Layout structure
        5. Visual hierarchy

        Be specific and modern. Focus on real-time polling UI."""),
        HumanMessage(content=f"Task: {state['task']}\n\nContext: live-polling project")
    ]

    response = llm.invoke(messages)
    state["design_concept"] = response.content
    return state

def html_css_expert(state: FrontendState):
    """Groq Qwen - HTML/CSS 생성"""
    console.print("[cyan]💻 HTML/CSS Expert (Qwen) coding structure...[/cyan]")

    llm = groq_qwen or gemini
    messages = [
        SystemMessage(content="""You are a senior frontend developer specializing in
        clean, semantic HTML and modern CSS. Based on the design concept, generate:
        1. Complete HTML structure (semantic tags)
        2. CSS with flexbox/grid layout
        3. Responsive design (mobile-first)
        4. CSS variables for theming

        Use vanilla HTML/CSS only. No frameworks. Include full working code."""),
        HumanMessage(content=f"""
        Design Concept:
        {state['design_concept']}

        Task: {state['task']}
        """)
    ]

    response = llm.invoke(messages)
    state["html_css"] = response.content
    return state

def animation_specialist(state: FrontendState):
    """Mistral - CSS/JS 애니메이션"""
    console.print("[cyan]✨ Animation Specialist (Mistral) adding animations...[/cyan]")

    llm = mistral or groq_llama
    messages = [
        SystemMessage(content="""You are a CSS/JS animation specialist. Add:
        1. CSS transitions and animations
        2. Keyframe animations
        3. Smooth micro-interactions
        4. Loading states
        5. Hover effects

        Make it smooth and performant. 60fps animations only."""),
        HumanMessage(content=f"""
        HTML/CSS Code:
        {state['html_css']}

        Task: {state['task']}
        """)
    ]

    response = llm.invoke(messages)
    state["animations"] = response.content
    return state

def javascript_developer(state: FrontendState):
    """Groq Llama - JavaScript 로직"""
    console.print("[cyan]⚡ JavaScript Developer (Llama) coding logic...[/cyan]")

    llm = groq_llama or gemini
    messages = [
        SystemMessage(content="""You are a JavaScript expert. Implement:
        1. Event handlers
        2. DOM manipulation
        3. Real-time data handling
        4. State management (vanilla JS)
        5. Error handling

        Clean, modern ES6+ code. No jQuery. Include Supabase integration."""),
        HumanMessage(content=f"""
        HTML/CSS:
        {state['html_css']}

        Animations:
        {state['animations']}

        Task: {state['task']}
        """)
    ]

    response = llm.invoke(messages)
    state["javascript"] = response.content
    return state

def ux_specialist(state: FrontendState):
    """Gemini - UX 리뷰"""
    console.print("[cyan]🔍 UX Specialist (Gemini) reviewing experience...[/cyan]")

    llm = gemini or groq_llama
    messages = [
        SystemMessage(content="""You are a UX specialist. Review and suggest:
        1. Accessibility improvements (WCAG 2.1)
        2. User flow optimization
        3. Error states and edge cases
        4. Mobile UX considerations
        5. Performance suggestions

        Be constructive and specific."""),
        HumanMessage(content=f"""
        HTML/CSS:
        {state['html_css']}

        JavaScript:
        {state['javascript']}

        Animations:
        {state['animations']}

        Task: {state['task']}
        """)
    ]

    response = llm.invoke(messages)
    state["ux_review"] = response.content
    return state

def integration_lead(state: FrontendState):
    """Codex - 최종 통합"""
    console.print("[cyan]🧩 Integration Lead (Codex) synthesizing...[/cyan]")

    llm = codex or gemini or groq_llama  # Prefer Codex, then fallbacks
    messages = [
        SystemMessage(content="""You are the technical lead. Create the final,
        production-ready code by:
        1. Integrating all components
        2. Optimizing for performance
        3. Adding comprehensive comments
        4. Creating clear file structure
        5. Writing implementation guide

        Output: Complete, ready-to-use HTML/CSS/JS code."""),
        HumanMessage(content=f"""
        Task: {state['task']}

        Design Concept:
        {state['design_concept']}

        HTML/CSS:
        {state['html_css']}

        Animations:
        {state['animations']}

        JavaScript:
        {state['javascript']}

        UX Review:
        {state['ux_review']}
        """)
    ]

    response = llm.invoke(messages)
    state["final_code"] = response.content
    return state

# Build graph
def create_frontend_team():
    workflow = StateGraph(FrontendState)

    # Add nodes
    workflow.add_node("design", visual_designer)
    workflow.add_node("html_css", html_css_expert)
    workflow.add_node("animation", animation_specialist)
    workflow.add_node("javascript", javascript_developer)
    workflow.add_node("ux", ux_specialist)
    workflow.add_node("integrate", integration_lead)

    # Define flow
    workflow.set_entry_point("design")
    workflow.add_edge("design", "html_css")
    workflow.add_edge("html_css", "animation")
    workflow.add_edge("html_css", "javascript")
    workflow.add_edge("animation", "ux")
    workflow.add_edge("javascript", "ux")
    workflow.add_edge("ux", "integrate")
    workflow.add_edge("integrate", END)

    return workflow.compile()

def main():
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold]🎨 AI Frontend Dream Team - LangGraph CLI[/bold]\n\n"
            "[yellow]Usage:[/yellow]\n"
            "  python ai-team.py \"<frontend task>\"\n\n"
            "[yellow]Examples:[/yellow]\n"
            "  python ai-team.py \"실시간 투표 UI 만들기\"\n"
            "  python ai-team.py \"반응형 답변 카드 디자인\"\n"
            "  python ai-team.py \"QR 스캔 모달 애니메이션\"\n\n"
            "[dim]Team: Gemini (Design) + Qwen (HTML/CSS) + Mistral (Animation) + Llama (JS) + Codex (Integration)[/dim]",
            border_style="cyan"
        ))
        sys.exit(0)

    task = " ".join(sys.argv[1:])

    console.print(Panel.fit(
        f"[bold cyan]🎨 AI Frontend Dream Team[/bold cyan]\n\n"
        f"[yellow]Task:[/yellow] {task}\n\n"
        f"[dim]Workflow: Design → HTML/CSS + Animation + JS → UX Review → Integration[/dim]",
        border_style="cyan"
    ))

    initial_state = {
        "task": task,
        "design_concept": "",
        "html_css": "",
        "animations": "",
        "javascript": "",
        "ux_review": "",
        "final_code": ""
    }

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="🎨 Frontend team collaborating...", total=None)

            graph = create_frontend_team()
            result = graph.invoke(initial_state)

        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ Frontend Code Ready![/bold green]",
            border_style="green"
        ))
        console.print("\n")
        console.print(Markdown(result["final_code"]))
        console.print("\n")
        console.print("[dim]💡 Copy the code and integrate into your project[/dim]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
