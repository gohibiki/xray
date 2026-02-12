from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line, String, Rect
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart

# Register the Open Sans Light font
pdfmetrics.registerFont(TTFont('OpenSansLight', "OpenSans-VariableFont_wdth,wght.ttf"))
pdfmetrics.registerFont(TTFont('GothamLight', "GothamLight.ttf"))

def calculate_discrete_performance(historical_prices, years=5):

    data = historical_prices.copy()
    data.index = pd.to_datetime(data.index)  # Ensure the index is in datetime format

    today = datetime.today().date()

    # Step 1: Create the list of periods for the last `years` number of years
    periods = []
    for i in range(years):
        end_date = today - timedelta(days=i * 365)
        start_date = end_date - timedelta(days=365)
        periods.append((start_date, end_date))

    # Step 2: Calculate performance for each period using the nearest available date
    performance_data = []
    for start, end in periods:
        try:
            # Use the nearest available date for both start and end
            start_price = data.asof(pd.Timestamp(start))
            if pd.isna(start_price):
                start_price = data.iloc[0]  # Fallback to the first available price if start_price is NaN
            end_price = data.asof(pd.Timestamp(end))
            performance = ((end_price - start_price) / start_price) * 100
            performance_data.append(performance)
        except KeyError:
            performance_data.append(None)  # Handle missing data by appending None

    # Step 3: Create the DataFrame
    discrete_performance_df = pd.DataFrame({
        'Period': [f"{start.month}/{start.year}\n{start.month}/{end.year}" for start, end in periods],
        'Performance': [f"{perf:.2f}%" if perf is not None else "N/A" for perf in performance_data]
    })

    # Step 4: Sort the DataFrame by Period (from older to recent)
    discrete_performance_df = discrete_performance_df.sort_values(by='Period', ascending=True).reset_index(drop=True)

    return discrete_performance_df

def get_monthly_returns_table(combined_portfolio):
    # Define the date range for the last 5 years
    start = (datetime.today() - timedelta(days=365 * 5)).strftime('%d%m%Y')
    end = datetime.today().strftime('%d%m%Y')
    
    # Fetch historical prices
    data = combined_portfolio

    # Convert index to datetime if necessary
    data.index = pd.to_datetime(data.index, format='%d%m%Y')
    
    # Resample to get the last price of each month
    monthly_prices = data.resample('ME').last()
    
    # Calculate monthly returns
    monthly_returns = monthly_prices.pct_change().dropna() * 100
    
    # Create a DataFrame for better visualization
    monthly_returns_df = monthly_returns.to_frame(name='Return')
    monthly_returns_df['Year'] = monthly_returns_df.index.year
    monthly_returns_df['Month'] = monthly_returns_df.index.strftime('%b')
    
    # Pivot the table to get years as rows and months as columns
    monthly_table = monthly_returns_df.pivot_table(index='Year', columns='Month', values='Return')
    
    # Sort the columns to have months in order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_table = monthly_table[month_order]

    # Calculate the Year-to-Date (YTD) return for each year
    ytd_returns = monthly_table.sum(axis=1).to_frame(name='Total')
    
    # Add YTD returns as a new column to the monthly returns table
    monthly_table = pd.concat([monthly_table, ytd_returns], axis=1)

    # Sort the table by Year from recent to old
    monthly_table = monthly_table.sort_index(ascending=False)
    
    # Format the table to show percentages with one decimal and add + sign for positive values
    monthly_table = monthly_table.map(lambda x: f"{x:+.1f}" if not pd.isnull(x) else "-")
    
    return monthly_table

# Function to create a bar chart for the discrete performance
def create_discrete_performance_chart(benchmark_df, df):
    drawing = Drawing(500, 110)
    bc = VerticalBarChart()
    bc.x = 17
    bc.y = 20
    bc.height = 86
    bc.width = 370

    # Portfolio performance data
    portfolio_data = df['Performance'].str.rstrip('%').astype('float').tolist()
    benchmark_data = benchmark_df['Performance'].str.rstrip('%').astype('float').tolist()

    bc.data = [portfolio_data, benchmark_data]

    # Set colors for portfolio and benchmark bars
    bc.bars[0].fillColor = colors.HexColor("#BA5C12")  # Color for portfolio bars
    bc.bars[0].strokeColor = None

    bc.bars[1].fillColor = colors.HexColor("#24306280")  # Grey color for benchmark bars
    bc.bars[1].strokeColor = None

    bc.categoryAxis.categoryNames = df['Period'].tolist()

    bc.valueAxis.valueMin = -25
    bc.valueAxis.valueMax = 60
    bc.valueAxis.valueStep = 25
    bc.barSpacing = 5
    bc.groupSpacing = 15 #10

    # Set bar labels for portfolio
    bc.barLabelFormat = '%0.2f%%'
    bc.barLabels.nudge = 10
    bc.barLabels.fontName = 'OpenSansLight'
    bc.barLabels.fontSize = 7
    bc.barLabels.boxAnchor = 'n'

    # Customize axes
    bc.valueAxis.visibleTicks = 0
    bc.valueAxis.visibleGrid = 1
    bc.valueAxis.gridStrokeDashArray = [2, 2]
    bc.valueAxis.visibleLabels = 0

    bc.categoryAxis.labels.dy = -40
    bc.categoryAxis.labels.fontName = 'OpenSansLight'
    bc.categoryAxis.labels.fontSize = 7
    bc.valueAxis.gridStrokeWidth = 0.5
    bc.valueAxis.gridStrokeColor = colors.darkgrey
    bc.valueAxis.strokeColor = colors.white
    bc.categoryAxis.strokeColor = colors.Color(1, 1, 1, alpha=0)

    bc.valueAxis.labels.fontName = 'OpenSansLight'
    bc.valueAxis.labels.fontSize = 7

    # Add custom labels manually
    y_pos = bc.y + (-22.5 - bc.valueAxis.valueMin) * (bc.height / (bc.valueAxis.valueMax - bc.valueAxis.valueMin))
    drawing.add(String(bc.x - 13, bc.y + (-3 - bc.valueAxis.valueMin) * (bc.height / (bc.valueAxis.valueMax - bc.valueAxis.valueMin)), "0%", fontName='OpenSansLight', fontSize=7, fillColor=colors.black))
    drawing.add(String(bc.x - 18, bc.y + (47 - bc.valueAxis.valueMin) * (bc.height / (bc.valueAxis.valueMax - bc.valueAxis.valueMin)), "50%", fontName='OpenSansLight', fontSize=7, fillColor=colors.black))

    # Draw x-axis line at -25
    x_axis_y = bc.y + (-38 - bc.valueAxis.valueMin) * (bc.height / (bc.valueAxis.valueMax - bc.valueAxis.valueMin))
    x_axis_line = Line(bc.x, x_axis_y, bc.x + bc.width, x_axis_y)
    x_axis_line.strokeColor = colors.darkgrey
    x_axis_line.strokeWidth = 0.5
    drawing.add(x_axis_line)

    # Draw dashed line at 0
    zero_line_y = bc.y + (0 - bc.valueAxis.valueMin) * (bc.height / (bc.valueAxis.valueMax - bc.valueAxis.valueMin))
    zero_line = Line(bc.x, zero_line_y, bc.x + bc.width, zero_line_y)
    zero_line.strokeColor = colors.darkgrey
    zero_line.strokeWidth = 0.5
    zero_line.strokeDashArray = [2, 2]
    drawing.add(zero_line)

    drawing.add(bc)
    return drawing

# Function to convert series data to line plot data
def convert_series_to_lineplot_data(series1, series2=None):
    data = []
    data1 = [(date.toordinal(), value) for date, value in zip(series1.index, series1)]
    data.append(data1)
    
    if series2 is not None:
        data2 = [(date.toordinal(), value) for date, value in zip(series2.index, series2)]
        data.append(data2)
    
    return data

# Function to create a line chart for fund performance
def create_fund_performance_chart(series1, series2=None):
    drawing = Drawing(500, 200)  # Adjusted the drawing size for full width
    lp = LinePlot()
    lp.x = 20
    lp.y = 20
    lp.height = 175
    lp.width = 518

    series1 = series1 * 100
    if series2 is not None:
        series2 = series2 * 100
    
    # Set line colors
    lp.lines[0].strokeColor = colors.HexColor("#BA5C12")
    if series2 is not None:
        lp.lines[1].strokeColor = colors.HexColor("#24306290")

    converted_data = convert_series_to_lineplot_data(series1, series2)
    lp.data = converted_data
    lp.joinedLines = 1
    lp.strokeColor = colors.white  # Hide top and right lines
    lp.lines.strokeWidth = 0  # Hide top and right lines

    lp.xValueAxis.valueMin = min(series1.index).toordinal()
    lp.xValueAxis.valueMax = max(series1.index).toordinal()
    lp.xValueAxis.strokeColor = colors.darkgrey  # Set x-axis color to dark grey
    lp.xValueAxis.gridStrokeColor = colors.darkgrey  # Set grid line color to dark grey
    lp.xValueAxis.visibleGrid = 1  # Show grid lines
    lp.xValueAxis.visibleTicks = 1
    lp.xValueAxis.visibleLabels = 1
    lp.xValueAxis.labels.fontName = 'OpenSansLight'
    lp.xValueAxis.labels.fontSize = 25/3
    lp.xValueAxis.labels.fillColor = colors.black  # Set x-axis labels to black
    lp.xValueAxis.gridStrokeWidth = 0.5  # Set x-axis grid line width
    lp.xValueAxis.gridStrokeDashArray = [2, 2]  # Set x-axis grid line dash pattern
    lp.xValueAxis.strokeWidth = 0.5  # Set x-axis line width

    # Custom x-axis labels
    years = range(series1.index.min().year + 1, series1.index.max().year + 1)
    x_labels = [pd.Timestamp(year=year, month=1, day=1).toordinal() for year in years]
    lp.xValueAxis.valueSteps = x_labels
    lp.xValueAxis.labels.textAnchor = 'middle'
    lp.xValueAxis.labelTextFormat = lambda x: str(pd.Timestamp.fromordinal(int(x)).year)

    lp.yValueAxis.valueMin = min(min(series1), min(series2) if series2 is not None else min(series1))
    lp.yValueAxis.valueMax = max(max(series1), max(series2) if series2 is not None else max(series1))
    lp.yValueAxis.strokeColor = colors.white
    lp.yValueAxis.gridStrokeColor = colors.darkgrey
    lp.yValueAxis.visibleGrid = 1
    lp.yValueAxis.visibleTicks = 0
    lp.yValueAxis.visibleLabels = 1
    lp.yValueAxis.labels.fontName = 'OpenSansLight'
    lp.yValueAxis.labels.fontSize = 25/3
    lp.yValueAxis.labels.fillColor = colors.black
    lp.yValueAxis.gridStrokeWidth = 0.5

    # Convert y-axis labels from base 100 to "10k" format
    lp.yValueAxis.labelTextFormat = lambda y: f"{(y/100)*10:.0f}k"

    drawing.add(lp)
    return drawing

def calculate_sri(historical_prices, sri_value=None):
    if sri_value is not None:
        return int(sri_value)

    # Calculate daily returns
    daily_returns = historical_prices.pct_change().dropna()

    # Calculate the standard deviation (volatility) of daily returns
    daily_volatility = np.std(daily_returns)

    # Annualize the daily volatility
    annualized_volatility = daily_volatility * np.sqrt(252) * 100  # 252 trading days in a year

    # Define the volatility intervals corresponding to the SRI scale
    volatility_intervals = [(0, 0.5), (0.5, 2), (2, 5), (5, 10), (10, 15), (15, 25), (25, np.inf)]

    # Determine the SRI based on the annualized volatility
    for sri_value, (lower_bound, upper_bound) in enumerate(volatility_intervals, start=1):
        if lower_bound <= annualized_volatility < upper_bound:
            return sri_value

# Function to create SRI (Synthetic Risk Indicator)
def create_sri(historical_prices, sri_value=None):

    sri_value = calculate_sri(historical_prices, sri_value)

    title = Paragraph("Synthetic Risk Indicator (SRI)", ParagraphStyle(
        name='Section', fontName='OpenSansLight', fontSize=10, leading=10, spaceAfter=0, textColor=colors.HexColor("#24306280")
    ))
    line = HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)
    risk_label = Paragraph("<font size=7>Lower Risk&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Higher Risk</font>", ParagraphStyle(name='Normal', fontName='OpenSansLight'))


    data = [["1", "2", "3", "4", "5", "6", "7"]]

    table_style = TableStyle([
        ('BACKGROUND', (sri_value-1, 0), (sri_value-1, 0), colors.HexColor("#24306280")),  # Highlight the calculated SRI level
        ('TEXTCOLOR', (sri_value-1, 0), (sri_value-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, -1), 'OpenSansLight', 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#24306280")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#24306280")),
    ])

    table = Table(data, colWidths=[7.75 * mm] * 7, rowHeights=[5 * mm])
    table.setStyle(table_style)

    return [[title], [line], [risk_label], [table], [Spacer(1, 2)]]

# Set up the PDF document
def create_pdf(combined_metrics_df, combined_portfolio, metrics_portfolio, investment_strategy, sri_value, combined_bench, additional_data, benchmark):
    output_path = "portfolio_report.pdf"
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=5, bottomMargin=5, leftMargin=5, rightMargin=5)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontName='GothamLight', fontSize=18, leading=15, spaceAfter=12, textColor=colors.HexColor("#24306280"))
    section_style = ParagraphStyle(name='Section', fontName='OpenSansLight', fontSize=10, leading=10, spaceAfter=0, textColor=colors.HexColor("#24306280"))
    normal_style = ParagraphStyle(name='Normal', fontName='OpenSansLight', fontSize=8)
    bottom_style = ParagraphStyle(name='Bottom', fontName='OpenSansLight', textColor=colors.darkgrey, fontSize=6, spaceBefore=0, spaceAfter=0, leading=7)
    footer_style = ParagraphStyle(name='Footer', fontName='OpenSansLight', fontSize=5, textColor=colors.darkgrey, leading=10)

    # Title
    logo_path = "logo.png"
    logo = Image(logo_path)
    logo.drawHeight = 0.6 * inch
    logo.drawWidth = logo.drawHeight * (1437 / 398)

    header_content = "<para spaceb='40'><b>Portfolio Report</b><br/><font size='12' color='darkgrey'>Date: {}</font></para>".format(
        datetime.today().strftime('%d.%m.%Y')
    )

    header_table = Table(
        [[Paragraph(header_content, title_style), logo]],
        colWidths=[403.84, 169.73]
    )

    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT')
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # Create fund performance chart and discrete performance chart
    fund_performance_chart = create_fund_performance_chart(combined_bench.resample('W').mean(), combined_portfolio.resample('W').mean())

    discrete_performance_df = calculate_discrete_performance(combined_portfolio, 5)
    discrete_performance_bench = calculate_discrete_performance(benchmark, 5)
    #discrete_performance_df['Period'] = discrete_performance_df['Period'].str.replace('-', '\n').str.replace(' ', '')
    discrete_performance_chart = create_discrete_performance_chart(discrete_performance_df, discrete_performance_bench)

    # Portfolio Holdings
    investment_strategy_content = [
        [Paragraph("Investment Strategy", section_style)],
        [HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)],
        [Paragraph(investment_strategy, normal_style)],
    ]

    # Create a table with one column to hold the content
    investment_strategy_table = Table(investment_strategy_content)
    elements.append(investment_strategy_table)
    elements.append(Spacer(1, 2))

    # Apply the grey background to the entire table
    #investment_strategy_table.setStyle(TableStyle([
    #    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey)
    #]))

    # Combined table for main content and additional sections
    left_table_data = []
    right_table_data = []

    # Append the table to the left_table_data
    #left_table_data.append([investment_strategy_table])
    left_table_data.append([Paragraph("Portfolio Holdings", section_style)])
    left_table_data.append([HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)])

    # Create a function to format cells in the first column
    def format_first_column(value):
        if ' ' in str(value):
            pct, rest = str(value).split(' ', 1)
            return Paragraph(f'<font color="#30617F">{pct}</font> {rest}',
                            ParagraphStyle('base', fontName='OpenSansLight', fontSize=8))
        return value

    # Format your data
    formatted_data = []
    for row in combined_metrics_df.values.tolist():
        # Format only the first column, keep other columns as is
        new_row = [format_first_column(row[0])] + list(row[1:])
        formatted_data.append(new_row)

    # Create table with your existing headers and formatted data
    header_level1 = ['', 'Yield', 'Cumulative Growth (%)', 'Cumulative Growth (%)', 'Cumulative Growth (%)', 'Annualized Growth (%)', 'Annualized Growth (%)', 'Annualized Growth (%)']
    header_level2 = ['', '', '1m', '3m', 'YTD', '1yr', '3yr', '5yr']
    holdings_data = [header_level1, header_level2] + formatted_data
    fixed_col_widths = [160, 32, 32, 32, 32, 32, 32, 32]
    holdings_table = Table(holdings_data, colWidths=fixed_col_widths)

    # Keep your existing table style
    holdings_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'OpenSansLight', 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.darkgrey),
        ('VALIGN', (1, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.HexColor("#24306280")),
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (2, 0), (4, 0)),
        ('SPAN', (5, 0), (7, 0)),
    ]))

    left_table_data.append([holdings_table])
    left_table_data.append([Spacer(1, 2)])

    # Fund Performance
    left_table_data.append([Paragraph("Fund Performance", section_style)])
    left_table_data.append([HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)])
    fund_performance_chart_image = Image(fund_performance_chart)
    fund_performance_chart_image.drawHeight = 2*inch
    fund_performance_chart_image.drawWidth = 5*inch
    left_table_data.append([fund_performance_chart_image])
    left_table_data.append([Paragraph('The Growth of 10,000 chart reflects a hypothetical 10,000 investment and assumes reinvestment of dividends and capital gains.' , bottom_style)])
    left_table_data.append([Spacer(0, 0.5)])

    performance_data = [metrics_portfolio.columns.tolist()] + metrics_portfolio.values.tolist()
    
    def create_square(color):
        size = 6
        drawing = Drawing(size, size)
        square = Rect(0, 0, size, size, fillColor=color, strokeColor=color)
        drawing.add(square)
        return drawing

    def create_square_with_text(square_color, text, text_style):
        square = create_square(square_color)
        paragraph = Paragraph(text, text_style)
        square_with_text_table = Table(
            [[square, paragraph]],
            colWidths=[10, 80],
            rowHeights=[7]
        )
        square_with_text_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'LEFT'),
            #('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (0, 0), 5)
        ]))
        return square_with_text_table

    performance_data[2][0] = create_square_with_text(colors.HexColor("#24306280"), "Portfolio", normal_style)
    performance_data[1][0] = create_square_with_text(colors.HexColor("#BA5C12"), "Benchmark", normal_style)

    # Create the headers for the table
    header2_level1 = ['', 'Yield', 'Volatility', 'Cumulative Growth (%)', 'Cumulative Growth (%)', 'Cumulative Growth (%)', 'Annualized Growth (%)', 'Annualized Growth (%)', 'Annualized Growth (%)']
    header2_level2 = ['', '', '', '1m', '3m', 'YTD', '1yr', '3yr', '5yr']
    performance_data = [header2_level1, header2_level2] + performance_data[1:]
    fixed_col_widths2 = [110, 40, 40, 32, 32, 32, 32, 32, 32]
    performance_table = Table(performance_data, colWidths=fixed_col_widths2)
    performance_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'OpenSansLight', 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.darkgrey),
        ('VALIGN', (1, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#24306280")),
        ('SPAN', (0, 0), (0, 1)),  # Span Holdings across both rows
        ('SPAN', (1, 0), (1, 1)),  # Span Yield vertically across both rows
        ('SPAN', (2, 0), (2, 1)),  # Span Volatility vertically across both rows
        ('SPAN', (3, 0), (5, 0)),  # Span Cumulative Growth horizontally
        ('SPAN', (6, 0), (8, 0)),  # Span Annualized Growth horizontally
    ]))
    left_table_data.append([performance_table])
    left_table_data.append([Paragraph(f'Benchmark: {metrics_portfolio.iloc[0,0]}', bottom_style)])
    left_table_data.append([Spacer(0, 0.5)])

    # Discrete Performance
    left_table_data.append([Paragraph("Historical Performance", section_style)])
    left_table_data.append([HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)])
    
    #sub_table_data = [[discrete_performance_chart]]
    #sub_table = Table(sub_table_data)
    #left_table_data.append([sub_table])
    left_table_data.append([discrete_performance_chart])
    left_table_data.append([Spacer(0, 5)])
    left_table_data.append([Paragraph('The performance quoted represents past performance and does not guarantee future results' , bottom_style)])
    #left_table_data.append([Spacer(0, 0.5)])
    
    # Expected Performance
    #left_table_data.append([Paragraph("Net Performance (in %)", section_style)])
    #left_table_data.append([HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)])
    #
    #monthly_data = get_monthly_returns_table(combined_portfolio)
    #monthly_data = monthly_data.reset_index()
    #monthly_data.columns = [""] + monthly_data.columns[1:].tolist()
    #monthly_data = [monthly_data.columns.tolist()] + monthly_data.values.tolist()
    #monthly_table = Table(monthly_data, colWidths=27.8, rowHeights=15)
    #monthly_table.setStyle(TableStyle([
    #    ('FONT', (0, 0), (-1, -1), 'OpenSansLight', 8),
    #    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
    #    ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.darkgrey),
    #    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    #    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    #    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    #    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#24306280")),
    #    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#24306280")),
    #]))
    #left_table_data.append([monthly_table])

    # SRI
    sri_content = create_sri(combined_portfolio, sri_value)
    for item in sri_content:
        right_table_data.append(item)

    # Additional sections
    for section, df in additional_data.items():
        right_table_data.append([Paragraph(section, section_style)])
        right_table_data.append([HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor("#24306280"), spaceBefore=0, spaceAfter=0)])
        section_data = df.values.tolist()
        section_table = Table(section_data, colWidths=[0.64 * 0.3 * A4[0], 0.23 * 0.3 * A4[0]])
        section_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'OpenSansLight', 8),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
            ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.darkgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT')
        ]))
        right_table_data.append([section_table])
        right_table_data.append([Spacer(1, 2)])

    left_table = Table(left_table_data)
    right_table = Table(right_table_data)

    main_table = Table([[left_table, right_table]], colWidths = [409.69, 175.58],rowHeights=[0])
    #main_table = Table([[right_table, left_table]], colWidths = [175.58, 409.69],rowHeights=[0])

    main_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'OpenSansLight', 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey)
    ]))
    elements.append(main_table)

    # Footer
    def add_footer(canvas, doc):
        width, height = A4
        margin = 0.2 * inch

        footer_style = ParagraphStyle(
            name='Footer',
            fontName='OpenSansLight',
            fontSize=5,
            textColor=colors.darkgrey,
            leading=8
        )
        footer_text = """Richelieu Wealth Solutions. All Rights Reserved. The information, data, analyses and opinions contained herein include the confidential and proprietary information of Richelieu Wealth Solutions may not be copied or
        redistributed, are provided solely for informational purposes are not warranted to be correct, complete, accurate or timely and the date of data published may
        vary from fund to fund. Richelieu Wealth Solutions shall not be responsible for any trading decisions, damages or other losses resulting from, or related to, this information, data, analyses or opinions or their use and that the information must
        not be relied upon by you the user without appropriate verification. No investment decision should be made in relation to any of the information provided other than on the advice of a
        professional financial advisor; past performance is no guarantee of future results; and the value and income derived from investments can go down as well as up."""

        footer_paragraph = Paragraph(footer_text, footer_style)

        footer_width, footer_height = footer_paragraph.wrap(width - 2 * margin, height)
        x_position = (width - footer_width) / 2
        y_position = 0.1 * inch

        footer_paragraph.drawOn(canvas, x_position, y_position)

    doc.build(elements, onFirstPage=add_footer)

if __name__ == "__main__":
    create_pdf()