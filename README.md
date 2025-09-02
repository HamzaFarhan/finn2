# Operate AI MVP - CFO in a Box

## Architecture Evolution

### Approach 1: Initial Brainstorming - Polars Functions Approach
Initially, we considered creating a comprehensive library of Polars functions for common Excel and financial operations. This approach would have provided:
- Direct Python-based financial calculations
- Excel-like function interfaces
- Type-safe data transformations

**Challenge Discovered:** This approach led to approximately 200 possible tools, creating an overwhelming and unwieldy system that would be difficult to maintain and use effectively.

### Approach 2: Pivot to DuckDB + SQL
We decided to go with SQL and leverage DuckDB's powerful SQL engine for financial analysis:
- **DuckDB Advantages:** Columnar storage, advanced analytics functions, native CSV integration
- **SQL Familiarity:** Leverages existing SQL knowledge for financial calculations
- **Performance:** Memory-optimized processing for large datasets
- **Flexibility:** Dynamic query generation vs. fixed function library

### Approach 3: Graph-Based SQL Architecture (cfo_graph.py)
We implemented the SQL approach using a complex graph-based workflow system:
- **Pydantic Graph:** State machine for agent interactions with SQL execution
- **Multiple Node Types:** RunSQLNode, WriteSheetNode, UserInteractionNode, TaskResultNode
- **Complex State Management:** GraphState with message history and attempt tracking
- **SQL Integration:** Graph nodes executing DuckDB queries

**Challenge Discovered:** The graph architecture was unnecessarily complex for our use case, adding overhead without significant benefits for the financial analysis workflows we needed to support.

### Approach 4: Simplified SQL Agent Architecture (finn.py)
We simplified to a clean agent-based architecture while keeping the SQL approach:
- **Single Agent:** Streamlined interaction model with direct SQL execution
- **DuckDB Integration:** Direct SQL queries without graph complexity
- **Planning Integration:** Systematic planning and execution tracking
- **Memory Integration:** Persistent learning across sessions

**Challenge Discovered:** Even with the simplified architecture, letting the agent create SQL queries of any complexity made it prone to mistakes and hard to debug. The agent would often perform multiple analytical steps in a single complex query, making it difficult to identify what went wrong and provide targeted corrections when errors occurred.

### Approach 5: Return to Polars Functions - Intermediate Implementation
We decided to do the hard work and actually implement the comprehensive Polars functions library we had initially considered but discarded. This proved to be a superior approach:

**Key Advantages:**
- **Predictable Trajectories:** Each function has a clear, single purpose making agent behavior more predictable
- **Debuggable Operations:** Individual function calls can be isolated, tested, and corrected independently
- **Iterative Feedback:** When a function fails, it's easy to identify the specific issue and provide targeted fixes
- **Granular Control:** Agent performs one logical step at a time, making the analysis process transparent
- **Tool Suggestion:** Clear mapping between user requests and appropriate function calls

**Function Categories Implemented:**
- Basic Arithmetic & Aggregation (SUM, AVERAGE, statistical functions)
- Conditional Aggregation & Counting (SUMIF, COUNTIFS, etc.)
- Lookup & Reference Functions (VLOOKUP, INDEX/MATCH, etc.)
- Logical & Error-Handling Functions
- Financial Functions (NPV, IRR, PMT, etc.)
- Date & Time Functions
- Statistical & Trend Analysis
- Data Transformation & Pivoting
- Cohort & Customer Analytics
- And many more specialized financial analysis functions

**Challenge Discovered:** While the Polars approach solved the debuggability problem, it created a new issue for our Excel-savvy target demographic. The results were computed using Polars and then exported to Excel as static values, meaning:
- **No Formula Transparency:** Users couldn't see or understand the underlying calculations
- **No Excel Editability:** Finance professionals couldn't modify, trace, or debug the formulas in their familiar Excel environment
- **Performance Overhead:** Generating workbooks after computation added significant time to analysis delivery
- **Lost Excel Benefits:** Users lost the ability to leverage Excel's built-in auditing, What-If analysis, and formula debugging tools

### Approach 6: Direct Excel Formula Generation - Current Implementation
We pivoted to generating native Excel formulas directly using OpenPyXL, creating workbooks that finance professionals can fully understand, trace, and modify:

**Key Advantages:**
- **Formula Transparency:** Every calculation is visible as a native Excel formula that users can inspect and understand
- **Excel-Native Experience:** Finance professionals can use familiar Excel tools for auditing, debugging, and What-If analysis
- **Real-Time Performance:** Workbooks are created with formulas during analysis, eliminating post-processing time
- **User Editability:** Finance teams can modify formulas, add their own calculations, and extend the analysis
- **Familiar Debugging:** Users can use Excel's built-in formula auditing tools (trace precedents, evaluate formula, etc.)
- **Institutional Knowledge:** Workbooks become self-documenting with transparent calculation methods

This approach combines the precision and debuggability of discrete functions with the transparency and familiarity that finance professionals expect from Excel-based analysis.

**Challenge Discovered:** While the Excel formula generation approach solved the transparency and user experience issues, we discovered that the agent became overwhelmed with too many tools to choose from. With ~50 Excel functions across 4 toolsets, the agent struggled with decision paralysis and tool selection overhead, as industry best practices recommend keeping tool counts under 20 for optimal agent performance.

### Approach 7: Two-Mode Agent with On-Demand Toolset Loading - Current Implementation
Building on the challenge identified in Approach 6, we completely rewrote the agent architecture to solve the tool selection overwhelm problem.

**The Solution:** We completely rewrote the agent architecture to implement a two-mode system with on-demand toolset loading:

**Two-Mode Architecture:**
1. **PLAN Mode:** Agent only sees tool docstrings and descriptions, not the actual tools
   - Creates systematic plans with user approval
   - Each step specifies which toolset(s) will be needed
   - No tool execution burden during planning phase

2. **ACT Mode:** Agent fetches and loads only the relevant toolset for each step
   - Uses `fetch_toolset()` to load specific toolsets on-demand
   - Only the tools for the current step are available for selection
   - Dramatically reduces cognitive load on the model

**Key Architectural Components:**
- **Mode Management:** `Mode.PLAN` and `Mode.ACT` enum states
- **Toolset Registry:** All toolsets registered but not loaded initially
- **On-Demand Loading:** `fetch_toolset()` loads specific toolsets when needed
- **Plan-Driven Execution:** Each plan step specifies required toolsets
- **Step-by-Step Tool Access:** Only relevant tools available at each execution step

**Benefits:**
- **Reduced Cognitive Load:** Agent chooses from <20 tools at any given time
- **Better Tool Selection:** More focused and accurate tool usage
- **Maintained Functionality:** Full access to all 200+ functions when needed
- **Clear Planning:** Systematic approach with toolset requirements specified upfront
- **Improved Performance:** Less decision paralysis, faster execution

This approach maintains all the benefits of comprehensive Excel formula generation while solving the tool selection overwhelm problem through intelligent architectural design.

## Current Architecture

### Core Components

#### 1. Two-Mode Financial Analysis Agent (`agent.py` + `toolset_agent.py`)
The main CFO agent with a dual-mode architecture:
- **PLAN Mode:** Creates systematic plans using only tool descriptions, no actual tool access
- **ACT Mode:** Executes plans step-by-step with on-demand toolset loading
- **Mode Management:** Automatic switching between planning and execution phases
- **Toolset Registry:** Four specialized toolsets (structure, formatting, formula, charts) with ~50 functions
- **On-Demand Loading:** `fetch_toolset()` loads only relevant tools for each step
- **Cognitive Load Optimization:** Never more than ~20 tools available at once

#### 2. Two-Mode Planning & Execution System
**PLAN Mode Tools:**
- `create_plan_steps()`: Creates user-approved sequential plans with toolset specifications
- `execute_plan_steps()`: Switches from PLAN to ACT mode after user approval
- `toolset_defs_instructions()`: Provides tool descriptions without loading actual tools
- `user_interaction()`: Handles clarifications and assumptions during planning

**ACT Mode Tools:**
- `fetch_toolset()`: Loads specific toolsets on-demand for current step
- `update_plan_steps()`: Tracks progress and marks completed steps with token efficiency
- `add_plan_step()`: Dynamically adds steps during analysis execution
- `load_plan_steps()`: Reviews current plan status and progress
- `task_result()`: Validates plan completion and delivers final results

**Key Innovation:** Mode-based tool availability ensures agents only see relevant tools at each phase, dramatically reducing cognitive load while maintaining full functionality access.

#### 3. Memory System (`memory_tools.py` + `memory_mcp.py`)
**Persistent Knowledge Graph:**
- **Entity-Based:** Stores business concepts, calculation methods, user preferences
- **Relationship Mapping:** Connects related financial concepts and methodologies
- **Cross-Session Learning:** Accumulates institutional knowledge across analyses
- **Automatic Storage:** Proactively captures insights without user prompts

**Memory Categories:**
- Business model insights and characteristics
- Validated calculation methodologies
- Data architecture patterns
- User preferences and feedback patterns
- SQL optimization patterns

#### 4. Four On-Demand Excel Toolsets (`excel_toolsets/`)
**Modular Toolset Architecture with On-Demand Loading:**

**Excel Structure Toolset (21 tools):**
- File operations, sheet management, data integration
- Pivot tables, data tables, autofilters, subtotals
- CSV-to-Excel conversion with automatic data type detection

**Excel Formula Toolset (14 tools):**
- Complete library of Excel-compatible formula functions
- Math, Statistical, Financial, Logical, Lookup, Date/Time, Text, and Info functions
- Cross-sheet references, nested functions, conditional formulas

**Excel Formatting Toolset (7 tools):**
- Professional styling, conditional formatting, visual presentation
- Color management, preset systems, range-based formatting

**Excel Charts Toolset (7 tools):**
- Chart creation with OpenPyXL native and Matplotlib integration
- Professional styling, data range validation, preset management

**Key Architecture Benefits:**
- **Selective Loading:** Only relevant toolset loaded per execution step
- **Full Functionality:** All ~50 Excel functions available when needed
- **Cognitive Optimization:** Maximum ~21 tools available at once
- **Real-time Validation:** Formula syntax and reference validation before application

#### 5. Excel Formula Function Library
**Comprehensive Excel Formula Implementation:**
- **4 Core Toolsets:** Formula generation, structure management, formatting, and charting
- **~50 Excel Functions:** Coverage of Excel's essential mathematical, statistical, financial, and logical functions
- **Formula Transparency:** Every operation generates visible, editable Excel formulas
- **Syntax Validation:** Real-time validation of formula syntax and function parameters
- **Cross-Sheet Support:** Advanced multi-sheet references and complex workbook structures
- **Professional Output:** Finance-ready workbooks with proper formatting and documentation

#### 6. Thinking Framework (`thinking.py`)
**Structured Reasoning:**
- `think()`: Internal reasoning and problem breakdown
- `analyze()`: Result evaluation and next action determination
- Iterative problem-solving workflow
- Confidence tracking and validation


### Technology Stack

- **Backend:** Python with Pydantic AI agents
- **Excel Generation:** OpenPyXL for direct Excel formula creation and workbook management
- **Formula Library:** 200+ native Excel formula functions with syntax validation
- **Memory System:** MCP (Model Context Protocol) server
- **LLM Integration:** Configurable model selection (Claude, GPT, Gemini)
- **Validation Engine:** Comprehensive formula syntax and function validation using formulas library
- **Chart Generation:** Dual approach with OpenPyXL native charts and Matplotlib integration
- **Logging:** Loguru for comprehensive system monitoring

## Key Features

### 1. Systematic Financial Analysis
- **Mandatory Planning Phase:** All analyses start with user-approved systematic plans
- **Progress Tracking:** Real-time updates on analysis completion status
- **Iterative Refinement:** User feedback integration throughout the process

### 2. Excel-Native Formula Analytics
- **Formula Transparency:** Each operation generates visible Excel formulas that users can inspect and modify
- **Native Excel Functions:** Direct generation of standard Excel formulas (SUM, VLOOKUP, IF, etc.)
- **Formula Validation:** Pre-validation ensures syntax correctness and function compatibility
- **Composable Formulas:** Complex analyses built by chaining validated Excel formula functions

### 3. Persistent Learning
- **Workspace Memory:** Shared knowledge across all analyses in a workspace
- **Business Model Adaptation:** Learns specific business patterns and rules
- **Calculation Validation:** Stores proven methodologies for reuse
- **User Preference Learning:** Adapts to communication and analysis preferences

### 4. User Experience Focus
- **Concise by Default:** Direct answers unless detailed analysis requested
- **Complete Execution:** Ensures all requested analysis components are delivered
- **Progress Transparency:** Clear visibility into analysis status and next steps

## Workflow Example

1. **User Request:** "Calculate ARPU for January 2023 customers by industry segment"
2. **PLAN Mode - Planning Phase:** 
   - Agent sees only tool descriptions, not actual tools
   - Creates systematic analysis plan specifying required toolsets for each step
   - `create_plan_steps()` formalizes the approved approach with toolset requirements
3. **Mode Switch:** `execute_plan_steps()` switches agent from PLAN to ACT mode
4. **ACT Mode - Execution Phase:**
   - **Step 1:** `fetch_toolset("excel_structure_toolset")` loads file and data management tools
   - **Step 2:** `fetch_toolset("excel_formula_toolset")` loads formula generation tools for ARPU calculations
   - **Step 3:** `fetch_toolset("excel_formatting_toolset")` loads styling and presentation tools
5. **Progressive Execution:** Each step uses only relevant tools (~7-21 tools max)
6. **Progress Updates:** `update_plan_steps()` marks each completed step with clear formula-level granularity
7. **Formula-Based Workbooks:** Real-time creation of Excel workbooks with transparent, editable formulas
8. **Task Completion:** `task_result()` validates all steps completed and delivers final results

**Key Architectural Advantage:** Agent never sees more than ~21 tools at once, eliminating decision paralysis while maintaining access to all ~50 Excel functions through intelligent on-demand loading.

## Excel Toolsets Architecture

### 1. Excel Formula Toolset (`excel_formula_toolset.py`)
**Core Formula Generation Engine:** 1,391 lines of comprehensive formula validation and generation

**Formula Categories:**
- **Date Functions:** DATE, DAY, HOUR, MINUTE, MONTH, NOW, SECOND, TIME, TODAY, WEEKDAY, YEAR
- **Financial Functions:** FV, IRR, NPV, PMT, PV with complete parameter validation
- **Logical Functions:** AND, FALSE, IF, IFERROR, NOT, OR, TRUE with nested condition support
- **Lookup Functions:** CHOOSE, COLUMN, COLUMNS, HLOOKUP, INDEX, INDIRECT, MATCH, OFFSET, ROW, ROWS, VLOOKUP
- **Math Functions:** ABS, ACOS, ASIN, ATAN, CEILING, COS, COUNTIF, COUNTIFS, EXP, LOG, MAX, MIN, POWER, ROUND, SUM, SUMIF, SUMIFS, SUMPRODUCT and 30+ more
- **Statistical Functions:** AVERAGE, AVERAGEIF, AVERAGEIFS, COUNT, COUNTA, COUNTBLANK, LARGE, MEDIAN, MODE, PERCENTILE, QUARTILE, RANK, SMALL, STDEV, VAR
- **Text Functions:** CHAR, CLEAN, CODE, CONCATENATE, EXACT, FIND, LEFT, LEN, LOWER, MID, PROPER, REPLACE, RIGHT, SEARCH, SUBSTITUTE, TEXT, TRIM, UPPER, VALUE
- **Info Functions:** ISBLANK, ISERROR, ISNUMBER, ISTEXT
- **Arithmetic Operations:** ADD, SUBTRACT, MULTIPLY, DIVIDE, POWER with multi-operand support
- **Comparison Operations:** =, <>, <, >, <=, >= with comprehensive validation
- **Nested Functions:** Support for complex nested function calls with parameter validation
- **Conditional Formulas:** Advanced IF statement generation with condition validation

**Advanced Features:**
- **Formula Validation Engine:** Pre-validates syntax, function names, cell references, and cross-sheet relationships
- **Cross-Sheet Support:** Handles 'Sheet!Range' references with validation of sheet existence
- **Range Translation:** Automatic formula translation for cell ranges with relative reference adjustment
- **Error Detection:** Comprehensive error checking for division by zero, invalid references, and malformed ranges
- **Expression Builders:** Helper functions for building complex COUNTIFS and division expressions

### 2. Excel Structure Toolset (`excel_structure_toolset.py`)
**Workbook and Data Management Engine:** 1,844 lines of comprehensive Excel structure management

**Core Capabilities:**
- **File Operations:** Create, load, and manage Excel workbooks with proper error handling
- **Sheet Management:** Add, delete, rename, copy sheets with validation and conflict resolution
- **Data Integration:** CSV to Excel conversion with automatic data type detection using Polars
- **Advanced Pivot Tables:** Complete pivot table creation with customizable layouts, aggregations, and styling
- **Data Tables:** Professional Excel table creation with auto-formatting and style options
- **AutoFilter:** Add filtering capabilities to data ranges
- **Subtotals:** Automatic subtotal generation with grouping and summary functions
- **Multi-File Operations:** Merge multiple Excel files and extract sheets to CSV
- **Metadata Management:** Comprehensive spreadsheet and sheet information retrieval

**Advanced Features:**
- **Polars Integration:** Automatic data type detection and conversion for optimal Excel formatting
- **Pivot Table Engine:** Support for complex pivot tables with multiple fields, custom aggregations, and professional styling
- **Data Type Intelligence:** Automatic detection of dates, numbers, and text with proper Excel formatting
- **Cross-Sheet Operations:** Copy sheets between workbooks with formatting preservation
- **Professional Formatting:** Auto-sizing columns and rows with data type-specific width adjustments

### 3. Excel Formatting Toolset (`excel_formatting_toolset.py`)
**Professional Styling and Conditional Formatting Engine:** 625 lines of advanced formatting capabilities

**Formatting Categories:**
- **Cell Formatting:** Background colors, font styles, sizes, and colors with Google Sheets compatibility
- **Conditional Formatting:** 9 condition types (GREATER_THAN, LESS_THAN, EQUAL, BETWEEN, TEXT_CONTAINS, CUSTOM_FORMULA, etc.)
- **Color Management:** Support for hex colors and Google-style RGB color objects
- **Preset System:** Create, save, and apply formatting presets for consistent styling
- **Range-Based Formatting:** Apply formatting to individual cells or ranges with sheet detection

**Advanced Features:**
- **Google Sheets Compatibility:** Automatic conversion from Google Sheets formatting to Excel
- **Range Parsing:** Intelligent parsing of 'Sheet!Range' specifications
- **Format Validation:** Comprehensive validation of color formats and condition parameters
- **Preset Management:** JSON-based preset storage system for reusable formatting configurations

### 4. Excel Charts Toolset (`excel_charts_toolset.py`)
**Professional Chart Creation Engine:** 872 lines of comprehensive visualization capabilities

**Chart Types:**
- **OpenPyXL Native Charts:** Column, Bar, Line, Pie, Area, Doughnut, Radar, Bubble, Stock, Surface
- **Matplotlib Integration:** Line, Bar, Pie, Histogram, Box, Heatmap, Violin, Density charts with style support

**Chart Features:**
- **Data Range Validation:** Automatic validation of chart data ranges and sheet references
- **Chart Positioning:** Precise chart placement and sizing with TwoCellAnchor positioning
- **Professional Styling:** Customizable titles, legends, and chart aesthetics
- **Cross-Sheet Data:** Support for charts referencing data from multiple sheets
- **Image Embedding:** Matplotlib charts embedded as high-quality images in Excel

**Advanced Capabilities:**
- **Chart Management:** List, update, and delete existing charts
- **Preset System:** Save and apply chart configuration presets
- **Dual Engine:** Choice between native Excel charts (editable) and Matplotlib charts (high-quality images)
- **Data Reference Management:** Dynamic updating of chart data sources

## Function Coverage Summary

**Total Functions Available:** ~50 Excel-compatible functions across all categories
- **Structure Management:** 21 tools (file operations, sheets, pivot tables, data tables)
- **Formula Generation:** 14 tools (math, statistical, financial, logical, lookup, date/time, text, info functions)
- **Formatting:** 7 tools (cell formatting, conditional formatting, styling presets)
- **Charts:** 7 tools (chart creation, styling, data management)
- **File Operations:** 3 tools (file listing, description, path resolution)

**Validation Coverage:** Every function includes comprehensive input validation, syntax checking, and error handling to ensure generated Excel formulas are syntactically correct and functionally sound.
