
import pandas as pd 
import plotly_express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_extras.dataframe_explorer import dataframe_explorer




class Airbnb():
    def __init__(self) -> None:
        hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)
        self.sidebar()
        self.context()

    def context(self):
        if self.selected == "Home":
            self.home()
        if self.selected == "Airbnb Dataset":
            self.dataset()
        if self.selected=="Data Exploration":
            self.exploration()
        if self.selected=="About":
            self.about()

    def sidebar(self):
        with st.sidebar:  
            image1=Image.open("img/Airbnb_icon .png")
            s1,l,s2 = st.columns([1,2,1])
            with l:
                st.image(image1,use_column_width=True)  

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            
            self.selected = option_menu("Main menu", ["Home", "Airbnb Dataset", "Data Exploration", 'About'], 
                icons=['app-indicator', 'file-bar-graph-fill', 'toggles', 'person-lines-fill'], key='menu_4', )

    def df_airbnb(self):
        df=pd.read_csv("Airbnb.csv")
        return df


    def home(self):

        st.markdown("<h1 style='color:white; text-align:center;'>AIRBNB Data Analysis</h1>", unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.write("")
        cc, ic = st.columns([3,2])
        with cc:
            st.markdown("### :violet[Domain :] Travel Industry, Property Management and Tourism ")
            st.markdown("### :violet[Technologies used :] Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb.")
            st.markdown("### :violet[Overview :] This is a streamlit web app you can visualize and  analyze Airbnb data and gain lot of insights on the property-types, Room-types, Rents and Reviews .")  
        with ic:
            image2=Image.open("img/airbnb_img.jpeg")
            st.image(image2,use_column_width=True) 

        st.write("---")

        st.markdown("<h1 style='color:white; text-align:center;'>Airbnb Presence in Different Countries</h1>", unsafe_allow_html=True)
        df = self.df_airbnb()
        df=df.rename(columns={"lati":"lat","longi":"lon"})
        st.map(df)
        st.write("---")

    def dataset(self):
        st.markdown("<h1 style='color:white; text-align:center;'>Explore the Airbnb dataset</h1>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        ex=pd.read_csv("Airbnb.csv")
        ex=ex[['host_name','Country','Room_type','Property_type','price','Minimum_nights','maximum_nights','cancellation_policy','bedrooms']]
        ft_df=dataframe_explorer(ex)
        st.dataframe(ft_df,use_container_width=True)

    def exploration(self):
        st.markdown("<h1 style='color:white; text-align:center;'>Airbnb Data Exploration</h1>", unsafe_allow_html=True)
        st.write("")
        st.write("#### Kindly Choose the Filtering Parameter")
        cl1,cl2,cl3=st.columns([1,2,1])
        df = self.df_airbnb()
        with cl1:
            country=st.multiselect("Select The Desire Country",sorted(df['Country'].unique()))
            if not country:
                df1=df.copy()
            else:
                df1=df[df['Country'].isin(country)]
        with cl2:
            pro_type=st.multiselect("Select The Desire Property_type",sorted(df['Property_type'].unique()))
            if not pro_type:
                df2=df1.copy()
            else:
                df2=df1[df1['Property_type'].isin(pro_type)]
        with cl3:
            room_ty=st.multiselect("Select The Desire Room_type",sorted(df['Room_type'].unique()))
            if not room_ty:
                df3=df2.copy()
            else:
                df3=df2[df2['Room_type'].isin(room_ty)]

        cl1,cl2=st.columns([1,1])
        with cl1:
            country_df=df3.groupby("Country").Id.count()
            country_df=country_df.reset_index()
            country_df=country_df.rename(columns={'Id':'Total_listed'})
            country_df=country_df.sort_values(by='Total_listed',ascending=True)
            fig=px.bar(country_df,x='Total_listed',y='Country',title='Countries with high Airbnb Listing',
                    color_discrete_sequence=px.colors.diverging.oxy)
            st.plotly_chart(fig)
        with cl2:
            Roomdf=df3.groupby('Room_type').Id.count()
            Roomdf=Roomdf.reset_index()
            Roomdf=Roomdf.rename(columns={'Id':'Total_listed'})
            label=Roomdf['Room_type']
            values=Roomdf['Total_listed']
            data = go.Pie(labels=label,values=values,hole=.5,title="Room Type Distribution", 
                                    marker=dict(colors= px.colors.diverging.oxy[:len(label)]))
            fig=go.Figure(data=[data])
            fig.update_layout(width=500,height=450)
            st.plotly_chart(fig)
        st.write("---")

        cl4,cl5=st.columns([1,1])
        with cl4:
            Roomdf=df3.groupby('Property_type').Id.count()
            Roomdf=Roomdf.reset_index()
            Roomdf=Roomdf.rename(columns={'Id':'Total_listed'})
            Roomdf=Roomdf.sort_values(by='Total_listed',ascending=True)
            fig=px.bar(Roomdf,x="Total_listed",y="Property_type",title="Property_type Distribution",color_discrete_sequence=px.colors.diverging.oxy)
            fig.update_layout(width=600,height=450)
            st.plotly_chart(fig)
        with cl5:
            cal_df=df3.groupby('cancellation_policy').Id.count()
            cal_df=cal_df.reset_index()
            cal_df=cal_df.rename(columns={'Id':'Total_listed'})
            label=cal_df['cancellation_policy']
            values=cal_df['Total_listed']
            data = go.Pie(labels=label,values=values,hole=.5,title="Cancellation_policy Distribution", marker=dict(colors= px.colors.diverging.oxy[:len(label)]))
            fig=go.Figure(data=[data])
            fig.update_layout(width=600,height=450)
            st.plotly_chart(fig)
        st.write("---")

        st.markdown("##")

        option = option_menu(menu_title ="", options=['Analysis by Price','Host Analysis By Review'], icons=['file-bar-graph-fill', 'file-bar-graph-fill'], default_index=0, orientation="horizontal")
        st.write("")
        st.write("")
        if option == "Analysis by Price":
            col1,col2=st.columns([1.5,1])
            with col1:
                #Average Price by Room Type
                price_Df=df3.groupby(['Country','Property_type','Room_type']).price.mean()
                price_Df=price_Df.reset_index()
                price_Df=price_Df.sort_values(by='price',ascending=True)
                fig=px.bar(price_Df,x='price',y='Country',title='Average Price distribution in Room type and Corresponding Countries',
                    color='Room_type', color_discrete_sequence=px.colors.diverging.oxy)
                st.plotly_chart(fig)
            with col2:
                st.write('Top 5 Average Price by Room Type and Property Type')
                price_Df1=price_Df.sort_values(by='price',ascending=True).reset_index()
                st.dataframe(price_Df1.head(6))

            #Average Price by Property Type
            fig=px.bar(price_Df,x='Property_type',y='price',title='Average Price distribution in Property type and Corresponding Countries',
                color='Country', color_discrete_sequence=px.colors.diverging.oxy)
            fig.update_layout(width=900,height=600)
            st.plotly_chart(fig)

            col1,col2=st.columns([1.5,1])
            with col1:
                #Pricing has High Review score
                price_review=df3[['Review_scores','price',"host_name"]].sort_values(by='price')
                fig=px.scatter(price_review,x='price',y='Review_scores',color='host_name',title='Price Distribution by Review Score', color_discrete_sequence=px.colors.diverging.oxy)
                st.plotly_chart(fig)
            with col2:
                st.write('Top 5 Average Price by Host Name Based On Review Score')
                price_review1=price_review.sort_values(by='price',ascending=True).reset_index()
                st.dataframe(price_review1.head(6))

            col1,col2=st.columns([1.5,1])
            with col1:
                #Pricing has High Number of Reviews
                price_review1=df3[['number_of_reviews','price',"host_name"]].sort_values(by='price')
                fig=px.scatter(price_review1,x='price',y='number_of_reviews',color='host_name',title='Price Distribution by Number of Review ', color_discrete_sequence=px.colors.diverging.oxy)
                st.plotly_chart(fig)
            with col2:
                st.write('Top 5 Average Price by Host Name Based On Number of Review')
                price_review2=price_review1.sort_values(by='price',ascending=True).reset_index()
                st.dataframe(price_review2.head(6))


        if option == "Host Analysis By Review":

            col1,col2=st.columns([1,1])
            with col1:
                #Review Scores by Host and Country
                re_sc=df3[['host_name','Review_scores','Country']]
                review_sc=re_sc.sort_values('Review_scores',ascending=False)
                fig = px.scatter(review_sc, x='Review_scores', y='host_name', color='Country', title='Review Scores by Host and Country',
                                labels={'Review_scores': 'Review Scores'}, color_discrete_sequence=px.colors.diverging.oxy)
                fig.update_layout(xaxis=dict(tickangle=45),width=550,height=450)
                st.plotly_chart(fig)
            with col2:
                re_sc1=re_sc.sort_values(by='Review_scores',ascending=False).reset_index()
                st.write("Top 5 Host Name by Score")
                st.dataframe(re_sc1.head(6))
            col1,col2=st.columns([1,1])
            with col1:
                #Review Scores by Host number of review and Country
                re_100=df3[['host_name','number_of_reviews','Country']]
                review_100=re_100.sort_values('number_of_reviews',ascending=False)
                review_100=review_100[review_100['number_of_reviews']>=250].sort_values('number_of_reviews',ascending=False)
                fig=px.bar(review_100,x='number_of_reviews',y='host_name',color='Country',title="High Number(>250) of Reviews by Host and Country", color_discrete_sequence=px.colors.diverging.oxy)
                fig.update_layout(width=550,height=450)
                st.plotly_chart(fig)
            with col2:
                re_101=re_100.sort_values(by='number_of_reviews',ascending=False).reset_index()
                st.write("Top 5 Host Name by Number of Review")
                st.dataframe(re_101.head(6))
        st.write("---")

        st.markdown("<h1 style='color:white; text-align:center;'>Geo-Visualization</h1>", unsafe_allow_html=True)
        fig = px.scatter_mapbox(df3, lat='lati', lon='longi', color='price', size='accommodates',
                                color_continuous_scale=px.colors.diverging.oxy,hover_name='Name', mapbox_style="carto-positron", zoom=0)
        fig.update_layout(width=1400,height=800,title='Geospatial Distribution of Listings')
        st.plotly_chart(fig)

    def about(self):
        st.markdown("<h1 style='color:white; text-align:center;'>AIRBNB </h1>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        option = option_menu(menu_title ="", options=['Overview of Airbnb.Inc','History of Airbnb'], icons=['app-indicator', 'app-indicator'], default_index=0, orientation="horizontal")
        st.write("")
        st.write("")
        
        if option == 'Overview of Airbnb.Inc':
            c1, c2 = st.columns([1,5])
            with c1:
                st.image("img/overview.jpg")
            with c2:
                st.write("")
                st.write("")
                st.markdown("<h2 style='color:white'> Overview </h2>", unsafe_allow_html=True)
                st.write('''Airbnb  operates an online platform for hospitality services. The company provides a mobile application (app) that enables users to list, discover, and book unique accommodations across the world. The app allows hosts to list their properties for lease, and enables guests to rent or lease on a short-term basis, which includes vacation rentals, apartment rentals, homestays, castles, tree houses and hotel rooms. The company has presence in China, India, Japan, Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy, Norway, Portugal, Russia, Spain, Sweden, the UK, and others. Airbnb is headquartered in San Francisco, California, the US.
                            ''')
        if option == 'History of Airbnb':
            c1, c2 = st.columns([7,5])
            with c1:
                st.write("")
                st.write("")
                st.markdown("<h2 style='color:white'> History of Airbnb </h2>", unsafe_allow_html=True)
                st.write('''In 2008, Brian Chesky (the current CEO), Nathan Blecharczyk, and Joe Gebbia, established the company now known as Airbnb. The idea blossomed after two of the founders started renting air mattresses in their San Francisco home to conference visitors. Hence, the original name of Airbed & Breakfast.In 2009, the name Airbnb was introduced and its offerings grew beyond air mattresses to include spare rooms, apartments, entire houses, and more. The locations in which it operated grew, as well. By 2011, Airbnb had opened an office in Germany and in 2013, it established a European headquarters in Dublin, Ireland. Its primary corporate location is still San Francisco.In addition to the U.S. and Europe, the company has established a presence in Australia, Asia, Cuba, as well as other nations (more than 220 countries and regions in total). It has also expanded its travel offerings to include local activities programs called Experiences
                            ''')
            with c2:
                st.image("img/history.png")
        st.write("---")
        st.subheader(":gray[My Contact]")
        st.subheader(":black[Project - Airbnb Data Anlysis]")
        st.link_button(":blue[LinkedIn]","www.linkedin.com/in/saravana-perumal-k-07233b1b4")
        st.link_button(":black[GitHub]","https://github.com/Saravana-kr22")

if __name__ == "__main__":
    st.set_page_config(page_title="AIRBNB.Inc DATA ANALYSIS",layout="wide",page_icon="img/Airbnb_icon .png",initial_sidebar_state='auto')
    Airbnb()