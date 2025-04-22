import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import subprocess
import os
import sys
import base64
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category
from behave.__main__ import main as behave_main
import shutil

def run_pytest(test_args):
    """Run pytest with given arguments"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cmd = ["pytest", "--cov=src"] + test_args.split()
    
    result = subprocess.run(
        cmd,
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONPATH": project_root}
    )
    return result.stdout or result.stderr

def generate_html_report():
    """Generate an HTML test report."""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        report_dir = os.path.join(project_root, "reports")
        os.makedirs(report_dir, exist_ok=True)
        
        subprocess.run([
            "pytest",
            "tests/",
            "--cov=src",
            "--html=reports/pytest_report.html",
            "--cov-report=html:reports/coverage",
            "--self-contained-html"
        ], check=True, cwd=project_root)
        
        return "HTML report generated successfully", os.path.join(report_dir, "pytest_report.html")
    except subprocess.CalledProcessError as e:
        return f"Report generation failed: {e.output}", None

def run_bdd_tests():
    """Run BDD tests and return output"""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        result = subprocess.run(
            ["behave", "features/", "--format", "pretty", "--outfile", "reports/bdd_report.txt"],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        output = result.stdout or result.stderr
        if os.path.exists(os.path.join(reports_dir, "bdd_report.txt")):
            with open(os.path.join(reports_dir, "bdd_report.txt"), "r") as f:
                output += "\n\n" + f.read()
        return output
    except Exception as e:
        return f"Error running BDD tests: {str(e)}"

def main():
    st.title("To-Do Application")
    
    # Testing section in sidebar
    st.sidebar.header("Testing")
    
    # Basic testing buttons
    if st.sidebar.button("Run Unit Tests"):
        output = run_pytest("tests/test_basic.py -v")
        st.code(output, language="bash")
    
    if st.sidebar.button("Run Parameterized Tests"):
        output = run_pytest("tests/test_advanced.py -k test_parametrized -v")
        st.code(output, language="bash")
    
    if st.sidebar.button("Run Mocking Tests"):
        output = run_pytest("tests/test_advanced.py -k test_mock -v")
        st.code(output, language="bash")
    
    if st.sidebar.button("Generate HTML Report"):
        status, report_path = generate_html_report()
        st.code(status, language="bash")
        if report_path and os.path.exists(report_path):
            with open(report_path, "rb") as f:
                st.download_button(
                    "Download Test Report",
                    f.read(),
                    file_name="pytest_report.html",
                    mime="text/html"
                )
    
    # TDD/BDD testing buttons
    st.sidebar.header("Advanced Testing")
    
    if st.sidebar.button("Run TDD Tests"):
        output = run_pytest("tests/test_tdd.py -v")
        st.code(output, language="bash")
    
    if st.sidebar.button("Run BDD Tests"):
        output = run_bdd_tests()
        st.code(output, language="bash")
        if "scenarios passed" in output.lower():
            st.success("BDD tests completed successfully!")
        else:
            st.error("Some BDD tests failed")

    # Load existing tasks
    tasks = load_tasks()
    
    # Display due soon notifications (TDD Feature 1)
    due_soon = [t for t in tasks 
               if not t["completed"] and "due_date" in t
               and 0 < (datetime.strptime(t["due_date"], "%Y-%m-%d") - datetime.now()).days <= 1]
    if due_soon:
        with st.expander("Due Soon Notifications"):
            for task in due_soon:
                st.warning(f"'{task['title']}' is due soon ({task['due_date']})")

    # Rest of your existing task management UI...
    # [Keep all your existing task creation/display/filtering code here]
    # ...

if __name__ == "__main__":
    main()