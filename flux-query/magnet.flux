import "strings"

from(bucket: "magnet")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "hdps")
  |> map(fn: (r) => ({ r with magnet: strings.toUpper(v: r.magnet) }))
  |> sort(columns: ["_time"], desc: true)
  |> unique(column: "_field")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> group(columns: [])
  |> sort(columns: ["order"])
  |> keep(columns: ["_time", "magnet", "cmon", "cset", "pol"])
