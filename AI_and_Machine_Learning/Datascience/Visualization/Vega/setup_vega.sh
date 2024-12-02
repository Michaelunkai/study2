#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to check if a command exists
command_exists () {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Create Project Directory
PROJECT_DIR="vega-project"

if [ -d "$PROJECT_DIR" ]; then
    echo "Directory '$PROJECT_DIR' already exists. Skipping creation."
else
    echo "Creating project directory '$PROJECT_DIR'..."
    mkdir "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Step 2: Initialize npm
if [ -f "package.json" ]; then
    echo "npm project already initialized. Skipping 'npm init'."
else
    echo "Initializing npm project..."
    npm init -y
fi

# Step 3: Install Vega and Vega-Embed
echo "Installing Vega and Vega-Embed..."
npm install vega vega-embed

# Step 4: Install live-server globally if not already installed
if command_exists live-server; then
    echo "live-server is already installed globally. Skipping installation."
else
    echo "Installing live-server globally..."
    sudo npm install -g live-server
fi

# Step 5: Create index.html with Vega Visualization
INDEX_FILE="index.html"

if [ -f "$INDEX_FILE" ]; then
    echo "File '$INDEX_FILE' already exists. Skipping creation."
else
    echo "Creating '$INDEX_FILE' with Vega visualization..."
    cat > "$INDEX_FILE" <<EOL
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Vega Visualization</title>
    <!-- Vega & Vega-Embed Scripts -->
    <script src="node_modules/vega/build/vega.min.js"></script>
    <script src="node_modules/vega-embed/build/vega-embed.min.js"></script>
</head>
<body>
    <h1>Vega Visualization Example</h1>
    <div id="vis"></div>

    <script type="text/javascript">
        const spec = {
            "\$schema": "https://vega.github.io/schema/vega/v5.json",
            "width": 400,
            "height": 200,
            "padding": 5,

            "data": [
                {
                    "name": "table",
                    "values": [
                        {"category": "A", "amount": 28},
                        {"category": "B", "amount": 55},
                        {"category": "C", "amount": 43},
                        {"category": "D", "amount": 91},
                        {"category": "E", "amount": 81},
                        {"category": "F", "amount": 53},
                        {"category": "G", "amount": 19},
                        {"category": "H", "amount": 87}
                    ]
                }
            ],

            "signals": [
                {
                    "name": "tooltip",
                    "value": {},
                    "on": [
                        {"events": "rect:mouseover", "update": "datum"},
                        {"events": "rect:mouseout", "update": "{}"}
                    ]
                }
            ],

            "scales": [
                {
                    "name": "xscale",
                    "type": "band",
                    "domain": {"data": "table", "field": "category"},
                    "range": "width",
                    "padding": 0.05,
                    "round": true
                },
                {
                    "name": "yscale",
                    "domain": {"data": "table", "field": "amount"},
                    "nice": true,
                    "range": "height"
                }
            ],

            "axes": [
                {"orient": "bottom", "scale": "xscale"},
                {"orient": "left", "scale": "yscale"}
            ],

            "marks": [
                {
                    "type": "rect",
                    "from": {"data": "table"},
                    "encode": {
                        "enter": {
                            "x": {"scale": "xscale", "field": "category"},
                            "width": {"scale": "xscale", "band": 1},
                            "y": {"scale": "yscale", "field": "amount"},
                            "y2": {"scale": "yscale", "value": 0}
                        },
                        "update": {
                            "fill": {"value": "steelblue"}
                        },
                        "hover": {
                            "fill": {"value": "red"}
                        }
                    }
                },
                {
                    "type": "text",
                    "encode": {
                        "enter": {
                            "align": {"value": "center"},
                            "baseline": {"value": "bottom"},
                            "fill": {"value": "#333"}
                        },
                        "update": {
                            "x": {"scale": "xscale", "signal": "tooltip.category", "band": 0.5},
                            "y": {"scale": "yscale", "signal": "tooltip.amount", "offset": -2},
                            "text": {"signal": "tooltip.amount"},
                            "fillOpacity": [
                                {"test": "datum === tooltip", "value": 0},
                                {"value": 1}
                            ]
                        }
                    }
                }
            ]
        };

        vegaEmbed('#vis', spec).then(function(result) {
            // Access the Vega view instance as result.view
        }).catch(console.error);
    </script>
</body>
</html>
EOL
fi

# Step 6: Start live-server in the background
echo "Starting live-server..."
live-server --port=8080 &

# Capture the process ID of live-server
LIVE_SERVER_PID=$!

# Give live-server a moment to start
sleep 2

# Echo the URL
echo "Vega visualization is running at: http://127.0.0.1:8080/"

# Optional: Wait for live-server to terminate
# Uncomment the following line if you want the script to wait
# wait $LIVE_SERVER_PID
