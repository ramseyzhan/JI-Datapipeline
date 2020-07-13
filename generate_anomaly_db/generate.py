f_in = open("abnormal.txt", "r")
f_out = open("data.sql", "w+")
while 1:
    line = f_in.readline()
    date = line.split()
    if line:
        recorded = date[0] + ' ' + date[1]
        fir_data_line = f_in.readline().split('[')[1]
        fir_data = fir_data_line.split()
        [global_active_power, global_reactive_power, voltage, global_intensity] = fir_data
        sec_data_line = f_in.readline().split(']')[0]
        sec_data = sec_data_line.split()
        [sub_metering_1, sub_metering_2, sub_metering_3] = sec_data
        f_out.write("INSERT INTO" + " anomaly (recorded, global_active_power, global_reactive_power, voltage, " +
              "global_intensity, sub_metering_1, sub_metering_2, sub_metering_3)\n" +
              "VALUES (\'" + recorded + "\', \'" + global_active_power + "\', \'" + global_reactive_power + "\', \'" + voltage + "\', \'" +
              global_intensity + "\', \'" + sub_metering_1 + "\', \'" + sub_metering_2 + "\', \'" + sub_metering_3 + "\');\n")
    else:
        break
