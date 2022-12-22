
f = open("data.c", "w")

f.write("#include \"main.h\"\n")
f.write("struct Blueprint bps[] = \n{\n")
num_bps = 0
for l in open("input").read().strip().splitlines():
    blueprint_id = l.split(":")[0].split(" ")[-1]
    robots = []
    a,b,c,d = l.split(":")[1][:-1].split(".")
    a = a[:-3].strip().split(" ")[-1]
    b = b[:-3].strip().split(" ")[-1]
    c = (c.split(" ore and ")[0].split(" ")[-1], c.split(" ore and ")[1].split(" ")[0])
    d = (d.split(" ore and ")[0].split(" ")[-1], d.split(" ore and ")[1].split(" ")[0])

    f.write(f"    {{ \n")
    f.write(f"        .id = {blueprint_id}, \n")
    f.write(f"        .ore_robot_cost = {{ .ore = {a} }}, \n")
    f.write(f"        .clay_robot_cost = {{ .ore = {b} }}, \n")
    f.write(f"        .obsidian_robot_cost = {{ .ore = {c[0]}, .clay = {c[1]} }}, \n")
    f.write(f"        .geode_robot_cost = {{ .ore = {d[0]}, .obsidian = {d[1]} }}, \n")

    f.write(" }, \n")

    num_bps += 1

f.write("};\n")

f.write(f"#define NUM_BPS       {num_bps}\n")