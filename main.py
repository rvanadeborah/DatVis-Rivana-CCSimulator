import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Loan Payment Simulator",
    page_icon="💳",
    layout="wide"
)

# =========================================================
# COLORS
# =========================================================

COLOR_MAIN = "Pink"          
COLOR_SECONDARY = "#60A4DB"     # Light Blue
COLOR_WARNING = "#9DBFDB"       # Blue
COLOR_DANGER = "#EF5350"        # Red
COLOR_INTEREST = "#9DBFDB"      # Blue
COLOR_PRINCIPAL = "#B39DDB"     # Lavender

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Poppins:wght@400;500;600&display=swap');

    /* Main background */
    .stApp {
        background-color: #F7F5F2;
    }

    /* Main content */
    .main {
        background-color: #F7F5F2;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #EFECF3;
    }

    section[data-testid="stSidebar"] * {
        font-family: 'Poppins', sans-serif;
    }

    /* Main text */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #302D35 !important;
    }

    p, div, span, label {
        font-family: 'Poppins', sans-serif;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border: 1px solid #E5E0E8 !important;
        box-shadow: 0px 4px 15px rgba(48, 45, 53, 0.06) !important;
    }

    /* Metric labels */
    div[data-testid="stMetricLabel"] {
        font-family: 'Poppins', sans-serif !important;
        color: #6A6570 !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }

    /* Metric values */
    div[data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        color: #302D35 !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    div[data-testid="stMetricValue"] > div {
        color: #302D35 !important;
        opacity: 1 !important;
    }

    div[data-testid="stMetricValue"] * {
        color: #302D35 !important;
        -webkit-text-fill-color: #302D35 !important;
        opacity: 1 !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER IMAGE
# =========================================================

try:
    st.image("header.png", use_container_width=True)
except:
    st.warning(
        "⚠️ header.png was not found. "
        "Please place your Canva PNG image in the same folder as main.py."
    )

# =========================================================
# INTRODUCTION
# =========================================================

st.title("Tell Us About Your Loan Could Look Like")

st.markdown(
    """
    Let’s see what happens to your money when you pay early, on time, or late — 
    pay early, pay right, or pay the price
    """
)

st.markdown(
    """
    Curious where your money actually goes?  

    """
)

st.markdown(
    """
    This simulator shows your balance, your interest, and your total payment —
    what you owe, what it grows, and where it goes
    """
)
# =========================================================
# SIDEBAR INPUT
# =========================================================

st.sidebar.header("💳 Loan Information")

principal = st.sidebar.number_input(
    "Original Principal (RM)",
    min_value=100.0,
    value=5000.0,
    step=100.0
)

annual_rate = st.sidebar.number_input(
    "Annual Interest Rate (%)",
    min_value=0.0,
    value=12.0,
    step=0.5
)

monthly_payment = st.sidebar.number_input(
    "Monthly Payment (RM)",
    min_value=10.0,
    value=300.0,
    step=10.0
)

payment_behavior = st.sidebar.selectbox(
    "Payment Behavior",
    ["Early", "On-time", "Late"]
)

# =========================================================
# LOAN SIMULATION FUNCTION
# =========================================================

def simulate_loan(
    principal,
    annual_rate,
    monthly_payment,
    payment_behavior
):

    balance = principal

    monthly_rate = annual_rate / 100 / 12

    # Payment behavior adjustments
    if payment_behavior == "Early":
        payment_factor = 1.10
        extra_interest = 0

    elif payment_behavior == "On-time":
        payment_factor = 1.00
        extra_interest = 0

    else:  # Late
        payment_factor = 0.90
        extra_interest = 0.02

    payment_amount = monthly_payment * payment_factor

    records = []

    total_interest = 0
    total_payment = 0

    month = 0

    while balance > 0 and month < 120:

        month += 1

        # Normal monthly interest
        interest = balance * monthly_rate

        # Additional interest for late payment
        if payment_behavior == "Late":
            interest += balance * extra_interest

        # Add interest to balance
        balance += interest

        # Payment
        payment = min(payment_amount, balance)

        balance -= payment

        # Avoid tiny negative numbers
        if balance < 0:
            balance = 0

        total_interest += interest
        total_payment += payment

        records.append(
            {
                "Month": month,
                "Interest": interest,
                "Payment": payment,
                "Remaining Balance": balance
            }
        )

    df = pd.DataFrame(records)

    return df, total_interest, total_payment, month


# =========================================================
# RUN SIMULATION
# =========================================================

df, total_interest, total_payment, payoff_months = simulate_loan(
    principal,
    annual_rate,
    monthly_payment,
    payment_behavior
)

# =========================================================
# METRICS
# =========================================================

st.markdown("## ⋞ Loan Summary ⋟")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Original Principal",
        value=f"RM {principal:,.2f}"
    )

with col2:
    st.metric(
        label="Total Interest",
        value=f"RM {total_interest:,.2f}"
    )

with col3:
    st.metric(
        label="Total Paid",
        value=f"RM {total_payment:,.2f}"
    )

with col4:
    st.metric(
        label="Payoff Time",
        value=f"{payoff_months} months"
    )

# =========================================================
# PAYMENT BEHAVIOR INFO
# =========================================================

if payment_behavior == "Early":

    st.success(
        "🌷 **Early Payment:** You are paying 10% more than the normal "
        "monthly payment, helping reduce the loan faster."
    )

elif payment_behavior == "On-time":

    st.info(
        "✨ **On-time Payment:** You are paying the standard monthly payment "
        "without additional penalties."
    )

else:

    st.warning(
        "⚠️ **Late Payment:** Your payment is 10% lower and an additional "
        "2% interest charge is applied monthly."
    )

# =========================================================
# VIEW 1 — LOAN BALANCE
# =========================================================

st.markdown("## 1. How Fast Does the Loan Balance Decrease?")

fig1 = px.line(
    df,
    x="Month",
    y="Remaining Balance",
    markers=True,
    title=f"Loan Balance Over Time — {payment_behavior} Payment"
)

fig1.update_traces(
    line=dict(
        color=COLOR_MAIN,
        width=4
    ),
    marker=dict(
        size=7
    )
)

fig1.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="#F7F5F2",
    font=dict(
        family="Poppins",
        color="#302D35"
    ),
    xaxis_title="Month",
    yaxis_title="Remaining Balance (RM)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================================================
# VIEW 2 — TOTAL INTEREST & COST COMPARISON
# =========================================================

st.markdown("## 2. Total Interest & Cost Comparison")

st.write(
    "See how different payment strategies affect the total "
    "interest you pay over the life of the loan."
)

# =========================================================
# RUN ALL THREE PAYMENT STRATEGIES
# =========================================================

early_df, early_interest, early_total, early_months = simulate_loan(
    principal,
    annual_rate,
    monthly_payment,
    "Early"
)

ontime_df, ontime_interest, ontime_total, ontime_months = simulate_loan(
    principal,
    annual_rate,
    monthly_payment,
    "On-time"
)

late_df, late_interest, late_total, late_months = simulate_loan(
    principal,
    annual_rate,
    monthly_payment,
    "Late"
)


# =========================================================
# CREATE COMPARISON DATA
# =========================================================

comparison_df = pd.DataFrame({
    "Payment Behavior": [
        "Early",
        "On-time",
        "Late"
    ],

    "Total Interest": [
        early_interest,
        ontime_interest,
        late_interest
    ]
})


# =========================================================
# CREATE BAR CHART
# =========================================================

fig2 = px.bar(
    comparison_df,
    x="Payment Behavior",
    y="Total Interest",
    text="Total Interest"
)


# =========================================================
# FORCE COLORS
# =========================================================

fig2.update_traces(
    marker_color=[
        COLOR_SECONDARY,   # Early = Light Blue
        COLOR_WARNING,     # On-time = Blue
        COLOR_DANGER       # Late = Red
    ],

    texttemplate="RM %{y:,.2f}",
    textposition="outside"
)


# =========================================================
# CHART DESIGN
# =========================================================

fig2.update_layout(
    title="Total Interest by Payment Strategy",

    xaxis_title="Payment Strategy",

    yaxis_title="Total Interest (RM)",

    plot_bgcolor="white",

    paper_bgcolor="#F7F5F2",

    font=dict(
        family="Poppins",
        color="#302D35"
    ),

    showlegend=False
)


st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# VIEW 3 — ORIGINAL PRINCIPAL VS CUMULATIVE PAYMENT
# =========================================================

st.markdown("## 3. Where Does Your Payment Go?")

df["Cumulative Paid"] = df["Payment"].cumsum()

fig3 = px.line(
    df,
    x="Month",
    y="Cumulative Paid",
    markers=True,
    title="Cumulative Payment Over Time"
)

fig3.update_traces(
    line=dict(
        color=COLOR_SECONDARY,
        width=4
    ),
    marker=dict(
        size=7
    )
)

fig3.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="#F7F5F2",
    font=dict(
        family="Poppins",
        color="#302D35"
    ),
    xaxis_title="Month",
    yaxis_title="Cumulative Payment (RM)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================================================
# PIE CHART
# =========================================================

st.markdown("## ⋞ Where Did All My Money Go? ⋟")

pie_df = pd.DataFrame(
    {
        "Category": [
            "Original Principal",
            "Interest"
        ],
        "Amount": [
            principal,
            total_interest
        ]
    }
)

fig4 = px.pie(
    pie_df,
    names="Category",
    values="Amount",
    title="Principal vs Interest"
)

fig4.update_traces(
    textinfo="label+percent",
    texttemplate="%{label}<br>RM %{value:,.2f}<br>%{percent}",
    hovertemplate="<b>%{label}</b><br>RM %{value:,.2f}<extra></extra>"
)

fig4.update_layout(
    paper_bgcolor="#F7F5F2",
    font=dict(
        family="Poppins",
        color="#302D35"
    )
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================================================
# INTERPRETATION
# =========================================================

st.markdown("## ⋞ What’s the Tea? ⋟")

if payment_behavior == "Early":

    st.markdown(
        f"""
        🌷 **You chose Early Payment.**

        By paying more each month, your loan is paid off in approximately
        **{payoff_months} months**.

        Your total interest is approximately:

        **RM {total_interest:,.2f}**

        Paying more earlier reduces the outstanding balance faster,
        which means less interest accumulates over time.
        """
    )

elif payment_behavior == "On-time":

    st.markdown(
        f"""
        ✨ **You chose On-time Payment.**

        Your loan is paid according to the standard monthly payment.
        The loan is paid off in approximately **{payoff_months} months**.

        Your total interest is approximately:

        **RM {total_interest:,.2f}**

        Consistent payments help keep the loan under control without
        additional late-payment charges.
        """
    )

else:

    st.markdown(
        f"""
        ⚠️ **You chose Late Payment.**

        Because the monthly payment is lower and an additional interest
        charge is applied, your loan takes approximately
        **{payoff_months} months** to pay off.

        Your total interest is approximately:

        **RM {total_interest:,.2f}**

        This shows how delayed payments can increase the overall cost
        of borrowing.
        """
    )

# =========================================================
# MONTHLY PAYMENT DETAILS
# =========================================================

st.markdown("## ⋞ Monthly Payment Details ⋟")

display_df = df.copy()

display_df["Interest"] = display_df["Interest"].map(
    lambda x: f"RM {x:,.2f}"
)

display_df["Payment"] = display_df["Payment"].map(
    lambda x: f"RM {x:,.2f}"
)

display_df["Remaining Balance"] = display_df["Remaining Balance"].map(
    lambda x: f"RM {x:,.2f}"
)

display_df["Cumulative Paid"] = display_df["Cumulative Paid"].map(
    lambda x: f"RM {x:,.2f}"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Built with Python + Streamlit + Plotly | "
    "Because watching debt disappear is kinda satisfying | "
    "Made By Rivana Deborah Satriani."
)
