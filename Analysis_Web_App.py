# Import Libraries
import pandas as pd
import plotly.express as px
import streamlit as st

# Start Building App
st.set_page_config(
    page_title="Analysis Portal", 
    page_icon="💻"
)

# Title
st.title(':green[Analyse Your Data]')
st.subheader(':rainbow[Explore Data With Ease]', divider='rainbow')

# Upload File
files = st.file_uploader('Upload CSV Or Excel File', type=['csv', 'xlsx'])

if files is not None:
    # Load Data
    if files.name.endswith('csv'):
        data = pd.read_csv(files)
    else:
        data = pd.read_excel(files)
    st.dataframe(data)
    st.info('File is Successfully Uploaded', icon='🔥')

    # Basic Info of Dataset
    st.subheader(':rainbow[Basic Information of Dataset]', divider='rainbow')

    # Adding Tabs
    tab1, tab2, tab3, tab4 = st.tabs(['Data Summary', 'Top and Bottom Rows', 'Data Types', 'Column Names'])

    with tab1:
        # Statistical Summary
        st.subheader(':blue[Statistical Summary of Dataset]')
        st.write(f'There are {data.shape[0]} Rows and {data.shape[1]} Columns')
        st.dataframe(data.describe())

    with tab2:
        # Top Rows
        st.subheader(':blue[Top Rows]')
        top_rows = st.slider('Number of Top Rows You Want', min_value=1, max_value=data.shape[0], key='Top_Slider')
        st.dataframe(data.head(top_rows))

        # Bottom Rows
        st.subheader(':blue[Bottom Rows]')
        bottom_rows = st.slider('Number of Bottom Rows You Want', min_value=1, max_value=data.shape[0], key='Bottom_Slider')
        st.dataframe(data.tail(bottom_rows))

    with tab3:
        # Column Datatypes
        st.subheader(':blue[Data Types of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        # Column Names
        st.subheader(':blue[Column Names]')
        st.dataframe(list(data.columns))

    # Unique Value Count
    st.subheader(':rainbow[Unique Value Count]', divider='rainbow')

    with st.expander('Values Count'):
        col1, col2 = st.columns(2)

        with col1:
            column = st.selectbox('Choose Column Name', options=list(data.columns))
        with col2:
            top_rows = st.number_input('Select Rows', min_value=1, step=1)
            st.write(f'Number of Maximum Unique Rows You Can Select is: {data[column].nunique()}')

        count = st.button('Count')

        if count:
            try:
                result = data[column].value_counts().reset_index().head(top_rows)
                st.dataframe(result)

                # Visualization
                st.subheader(':blue[Visualization]', divider='green')

                # Bar Chart
                st.subheader(':green[Bar Chart]')
                fig = px.bar(data_frame=result, x=column, y='count', text='count', template='plotly_dark')
                st.plotly_chart(fig)

                # Line Chart
                fig = px.line(data_frame=result, x=column, y='count', text='count', template='ggplot2')
                st.plotly_chart(fig)

                # Pie Chart
                fig = px.pie(data_frame=result, names=column, values='count', template='presentation')
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"An error occurred while processing the data: {e}")

    # Group By Function
    st.subheader(':rainbow[Group By : Simplify Your Data Analysis]', divider='rainbow')
    st.write("""The GroupBy Option in pandas is used to split a DataFrame into groups based on specified criteria. 
                This allows you to perform aggregate functions like sum, mean, or count on the grouped data, 
                facilitating complex data analysis.""")

    with st.expander('Grouping Your Columns'):
        col1, col2, col3 = st.columns(3)

        # Column Selection for GroupBy and Operations
        with col1:
            groupby_cols = st.multiselect('Choose Columns to Group By', options=list(data.columns))
        with col2:
            operation_cols = st.selectbox('Choose Column for Operation', options=list(data.columns))
        with col3:
            operation = st.selectbox('Select Operation', 
                                     options=['count', 'sum', 'mean', 'median', 'min', 'max', 'std', 'var', 
                                              'nunique', 'describe', 'quantile (Q1)', 'quantile (Q2)', 'quantile (Q3)', 
                                              'idxmin', 'idxmax'])

        # Explain Selected Operation
        operation_descriptions = {
            'count': 'Count of non-NA/null values in each group',
            'sum': 'Sum of values in each group',
            'mean': 'Mean (average) of values in each group',
            'median': 'Median (50th percentile) of values in each group',
            'min': 'Minimum value in each group',
            'max': 'Maximum value in each group',
            'std': 'Standard deviation of values in each group',
            'var': 'Variance of values in each group',
            'nunique': 'Number of unique values in each group',
            'describe': 'Descriptive statistics for each group',
            'quantile (Q1)': 'First quantile (25th percentile) in each group',
            'quantile (Q2)': 'Second quantile (50th percentile, Median) in each group',
            'quantile (Q3)': 'Third quantile (75th percentile) in each group',
            'idxmin': 'Index of the minimum value in each group',
            'idxmax': 'Index of the maximum value in each group'
        }

        if operation in operation_descriptions:
            st.write(operation_descriptions[operation])

        # Execute Operation
        if groupby_cols:
            grouped = data.groupby(groupby_cols)[operation_cols]
            try:
                if operation == 'quantile (Q1)':
                    result = grouped.quantile(0.25)
                elif operation == 'quantile (Q2)':
                    result = grouped.quantile(0.50)
                elif operation == 'quantile (Q3)':
                    result = grouped.quantile(0.75)
                else:
                    result = getattr(grouped, operation)().reset_index()

                # Display Result
                st.dataframe(result)

            except AttributeError:
                st.error(f"Operation '{operation}' is not supported on the selected column.")

            # Group By Visualization Section
            st.subheader(':green[Interactive GroupBy Visualization]', divider='blue')

            # User selects chart type
            chart = st.selectbox('Choose Your Plot Type', options=['Bar', 'Pie', 'Line', 'Scatter', 'Sunburst'])

            # Interactive visualization
            try:

                if chart == 'Bar':
                    x_axis = st.selectbox('Choose x-axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose y-axis', options=list(result.columns))
                    color = st.selectbox('Choose Color (Optional)', options=[None] + list(result.columns))
                    facet_col= st.selectbox('Divide Plot', options=[None] + list(result.columns))
                    fig= px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group', title='Bar Chart: Grouped Visualization')
                    st.plotly_chart(fig)

                elif chart == 'Pie':
                    names = st.selectbox('Choose Column', options=list(result.columns))
                    values = st.selectbox('Numerical Column', options=list(result.columns))
                    fig = px.pie(data_frame=result, names=names, values=values, title='Pie Chart: Grouped Visualization', template='presentation') 
                    st.plotly_chart(fig)      

                elif chart == 'Line':
                    x_axis = st.selectbox('Choose x-axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose y-axis', options=list(result.columns))
                    color = st.selectbox('Choose Color (Optional)', options=[None] + list(result.columns))                         
                    fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers='o', title='Line Chart: Grouped Visualization')
                    st.plotly_chart(fig)

                elif chart == 'Scatter':
                    x_axis = st.selectbox('Choose x-axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose y-axis', options=list(result.columns))
                    color = st.selectbox('Choose Color (Optional)', options=[None] + list(result.columns)) 
                    size= st.selectbox('Markers Size (Optional)', options=[None] + list(result.columns))               
                    fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size, title='Scatter Plot: Grouped Visualization')
                    st.plotly_chart(fig)

                elif chart == 'Sunburst':
                    x_axis = st.multiselect('Select Multiple Categorical Columns', options=list(result.columns))  
                    y_axis = st.selectbox('Select Numerical Column', options=list(result.columns))
                    color = st.selectbox('Choose Color (Optional)', options=[None] + list(result.columns))                       
                    fig = px.sunburst(data_frame=result, path=x_axis, values=y_axis, color=color, title='Sunburst Chart: Hierarchical Data', template='seaborn')
                    st.plotly_chart(fig)

            except Exception as e:
                        st.error(f"An error occurred while generating the {chart} chart. Details: {e}")

               
