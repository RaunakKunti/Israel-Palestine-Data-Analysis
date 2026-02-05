import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt

st.sidebar.title("Upload Dataset")
upload_file = st.sidebar.file_uploader("coose CSV file",type='csv')

if upload_file is not None:
    #Data preprocessing
    df = pd.read_csv(upload_file)
    no_event = len(df)

    df['age']=df['age'].fillna(df['age'].median())
    df=df.dropna(subset=['notes'])
    df['took_part_in_the_hostilities'] = df['took_part_in_the_hostilities'].fillna('Unknown')
    df['ammunition'] = df['ammunition'].fillna('Unknown')
    df['place_of_residence_district'] = df['place_of_residence_district'].fillna('Unknown')
    df['place_of_residence'] = df['place_of_residence'].fillna('Unknown')
    df['took_part_in_the_hostilities'] = df['took_part_in_the_hostilities'].fillna('Unknown')
    df['type_of_injury'] = df['type_of_injury'].fillna('Unknown')

    #important information
    citizenship_count = df['citizenship'].value_counts()
    event_location_region_count = df['event_location_region'].value_counts()
    hostalities_count = df[df['took_part_in_the_hostilities']=='Yes']['citizenship'].value_counts()
    no_hostalities_count = df[df['took_part_in_the_hostilities']=='No']['citizenship'].value_counts()
    st.sidebar.write("No of Events :",no_event)

    col1,col2 = st.sidebar.columns(2)
    col3,col4 = st.sidebar.columns(2)
    with col1:
        st.subheader("citizenship_counts")
        st.write(citizenship_count)
    with col2:
        st.subheader("event_location_region")
        st.write(event_location_region_count)
    with col3:
        st.subheader("hostalities_count")
        st.write(hostalities_count)
    with col4:
        st.subheader("no_hostalities_count")
        st.write(no_hostalities_count)
    
    #Body part
    st.title("Israel Palestine Conflict Analysis 2000-2023")
    st.subheader("Actual dataset")
    st.write(df)
    st.subheader("Fatalities per Year")
    df = df.copy()
    # Convert date column to datetime
    df['date_of_event'] = pd.to_datetime(df['date_of_event'], errors='coerce')

    # Extract year
    df['year'] = df['date_of_event'].dt.year
    fatalities_per_year = (
        df
        .groupby('year')
        .size()
        .reset_index(name='Deaths')
        .sort_values('year')
    )
    # Plot
    plt.figure(figsize=(5, 4))
    plt.plot(
        fatalities_per_year['year'],
        fatalities_per_year['Deaths'],
        marker='o'
    )

    plt.xlabel('Year')
    plt.ylabel('Number of Deaths')
    plt.title('Fatalities per Year (Israel–Palestine Conflict)')
    plt.grid(True)

    st.pyplot(plt)

    #types of weapon and gender ratio
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Type of Injuries")
        type_of_injury = df["type_of_injury"].value_counts()
        st.bar_chart(type_of_injury)
    with col2:
        st.subheader("Genderwise Fatalities Distribution")
        gender_count = df["gender"].value_counts()
        fig,ax=plt.subplots()
        ax.pie(gender_count,labels=gender_count.index,autopct='%1.1f%%')
        st.pyplot(fig)

        
    st.subheader("Geographic Distribution of Events")
    geographic_distribution_graph = (
    df["event_location_region"]
    .value_counts()
    .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(
        geographic_distribution_graph.index,
        geographic_distribution_graph.values
    )

    plt.xlabel('Region')
    plt.ylabel('Number of Events')
    plt.title('Geographic Distribution')

    st.pyplot(plt)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Age Distribution")
        plt.figure()
        df["age"].plot(kind="hist", bins=10)
        plt.xlabel("Age")
        plt.ylabel("Frequency")
        plt.title("Victim's Age Distribution")
        st.pyplot(plt)
    with col2:
        st.subheader("Average Age by Event Region")
        avg_age = df.groupby("event_location_region")["age"].mean()
        st.bar_chart(avg_age)

    st.subheader("Killed By")
    kill=df.groupby(df["killed_by"]).size()
    fig,ax=plt.subplots()
    ax.pie(kill,labels=kill.index,autopct='%1.1f%%')
    st.pyplot(fig)

    st.subheader("Types of Ammunition")
    Ammunition_count = df.groupby(df["ammunition"]).size()
    st.write(Ammunition_count)

