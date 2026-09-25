import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def apply_chart_dark_styles():
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = '#131520'
    plt.rcParams['axes.facecolor'] = '#181b28'
    plt.rcParams['axes.edgecolor'] = '#262930'
    plt.rcParams['grid.color'] = '#262930'
    plt.rcParams['text.color'] = '#e6e6fa'

def render_notes_distribution_chart(word_counts):
    apply_chart_dark_styles()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    
    if len(word_counts) > 0:
        sns.histplot(word_counts, kde=True, color='#06b6d4', ax=ax, bins=15)
    else:
        ax.text(0.5, 0.5, 'No notes uploaded yet', ha='center', va='center')
        
    ax.set_title('Word Density Distribution across Digitized Documents', fontsize=10, pad=10)
    ax.set_xlabel('Word Count', fontsize=8)
    ax.set_ylabel('Frequency', fontsize=8)
    ax.tick_params(labelsize=8)
    
    st.pyplot(fig)
    plt.close()

def render_approval_ratio_donut(approved_count, rejected_count):
    apply_chart_dark_styles()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    
    sizes = [approved_count, rejected_count]
    labels = ['Approved', 'Needs Review']
    colors = ['#10b981', '#ef4444']
    
    if sum(sizes) > 0:
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
               startangle=90, pctdistance=0.75, textprops={'fontsize': 8})
        centre_circle = plt.Circle((0,0), 0.55, fc='#131520')
        fig.gca().add_artist(centre_circle)
    else:
        ax.text(0.5, 0.5, 'No verification logs available', ha='center', va='center')
        
    ax.set_title('Document Repository Approval Status Matrix', fontsize=10, pad=10)
    st.pyplot(fig)
    plt.close()