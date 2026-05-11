import pandas as pd


df=pd.read_excel("Change Management Tracker (1).xlsx")

df.head()
df.keys()

# Total ECNs
print("Total ECNs:", len(df))

# Open ECNs
print("Open ECNs:", len(df[df["Delay Status"]=="Open"]))

# Closed ECNs
print("Closed ECNs:", len(df[df["Delay Status"]=="Closed"]))

# Delayed ECNs
print("Delayed ECNs:", len(df[df["Delay Status"]=="Delayed"]))

import matplotlib.pyplot as plt
df["Open Points-Team"].value_counts().plot(kind="pie", color="Red")
plt.title("ECN by Department")
plt.ylabel("Count")
plt.show()
df["Approval Pending"].value_counts().plot(kind="bar", color="black")
plt.title("ECN by Department")
plt.ylabel("Count")
plt.show()

# ECN by status
df["Status"].value_counts().plot(kind="bar", color="Orange")
plt.title("ECN Status Distribution")
plt.ylabel("Count")
plt.show()

df["Dept"].value_counts().plot(kind="bar")
plt.title("ECN by Department")
plt.ylabel("Count")
plt.show()

df["Date Raised"] = pd.to_datetime(df["Date Raised"],  errors="coerce")

monthly = df.groupby(df["Date Raised"].dt.to_period("M")).size()

monthly.plot(kind="bar", color="green")
plt.title("Monthly ECN Trend")
plt.ylabel("Number of ECNs")
plt.xticks(rotation=45)
plt.show()

df["Affected Area / Equipment"].value_counts().head(10).plot(kind="pie",color="brown")
plt.title("ECN Owners")
plt.xticks(rotation=90)
plt.show()











import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel
df = pd.read_excel("Change Management Tracker (1).xlsx")
df.columns = df.columns.str.strip()

# Replace blanks with empty string
df = df.fillna("")

# Convert filter columns to string
filter_cols = ["Dept", "Status", "Affected Area / Equipment"]

for col in filter_cols:
    df[col] = df[col].astype(str)

# Title
st.title("Change Management Dashboard")
st.caption("Live tracker for Engineering Change Notices and Process Changes")
st.sidebar.title("Filters")

dept = st.sidebar.selectbox(
    "Department",
    ["All"] + list(df["Dept"].dropna().unique())
)

status = st.sidebar.selectbox(
    "Status",
    ["All"] + list(df["Status"].dropna().unique())
)
area = st.sidebar.selectbox(
    "Equipment Owner",
    ["All"] + sorted(df["Affected Area / Equipment"].unique())
)


# Apply filters
filtered_df = df.copy()

if dept != "All":
    filtered_df = filtered_df[filtered_df["Dept"] == dept]

if status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status]
if filtered_df.empty:
    st.warning("⚠️ No ECNs found for the selected filters.")
    st.stop()

# KPI metrics
st.metric("Total ECNs", len(df))
st.metric("ECNs Open", len(df[df["ECN Status"]=="Open"]))
st.metric("ECNs ongoing Approval ", len(df[df["ECN Status"]=="ECR-Sign off Ongoing"]))
st.metric("ECNs upcoming ", len(df[df["ECN Status"]=="—"]))
st.metric("ECNs closed ", len(df[df["ECN Status"]=="closed"]))

filtered_df["Target Date"] = pd.to_datetime(
    filtered_df["Target Date"],
    errors="coerce"
)

overdue = filtered_df[
    (filtered_df["Target Date"] < pd.Timestamp.today()) &
    (filtered_df["Status"] != "Closed")
]

st.error(f"Overdue ECNs: {len(overdue)}")

# ------------------------
# Plot 1: Status Pie Chart
# ------------------------
st.subheader("Status")

fig1, ax1 = plt.subplots()
filtered_df["Status"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax1
)
ax1.set_ylabel("")
st.pyplot(fig1)

# ------------------------
# Plot 2: Department Bar
# ------------------------
st.subheader("ECN by Department")

fig2, ax2 = plt.subplots()
filtered_df["Dept"].value_counts().plot(
    kind="bar",
    ax=ax2
)
st.pyplot(fig2)

# ------------------------
# Plot 3: Priority
# ------------------------
st.subheader("ECN Owners")

fig3, ax3 = plt.subplots()
filtered_df["Affected Area / Equipment"].value_counts().head(10).plot(kind="pie",color="brown", ax=ax3)
st.pyplot(fig3)
# ------------------------
# Full Table
# ------------------------
df = pd.read_excel("Change Management Tracker (1).xlsx")

st.subheader("ECR Table")

st.dataframe(
    filtered_df[["ECN/PCN No", "ECN Title / Description", "Dept",
       "Details of changes required(Before)",
       "Details of changes required(After)", "Reason for Change",
       "Affected Area / Equipment", "Document Ref"]],
    column_config={
        "ECR Link": st.column_config.LinkColumn(
            "Open ECR",
            display_text="View"
        )
    },
    use_container_width=True
)

