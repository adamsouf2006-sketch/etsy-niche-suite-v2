set -e
cd "$(dirname "$0")"
python3 build_xlsx.py out_example.xlsx >/dev/null; python3 build_xlsx.py out_blank.xlsx --blank >/dev/null
soffice --headless --convert-to xlsx --outdir rc out_example.xlsx >/dev/null 2>&1
for x in "Dashboard B1:I27 dash" "Budget B1:F47 budget" "Habits B1:AJ20 habits" "Money Log B1:G24 log" "Savings & Debt B1:G38 savings" "Tasks B1:G18 tasks" "Cleaning B1:G24 cleaning" "Calendar B1:H18 calendar" "Meals B1:I24 meals" "Annual B1:O45 annual" "Goals B1:F24 goals" "Week Plan B1:I25 week" "Setup B1:F32 setup" "Start Here B1:C22 start"; do set -- $x; n=${@: -1}; r=${@: -2:1}; sh="${x% $r $n}"; python3 render_sheet.py "$sh" $r r/$n.html; done
args=""; for n in dash budget habits log savings tasks cleaning calendar meals annual goals week setup start; do args="$args $PWD/r/$n.html $PWD/r/$n.png"; done; python3 shot.py 1600 900 $args
