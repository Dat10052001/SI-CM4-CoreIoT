import React, { useState } from 'react';
import { View, Text, StyleSheet, Switch, Pressable, ScrollView } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const screenWidth = Dimensions.get('window').width;
const farm1 = {
    name: 'nong trai dang mo',
    ID: 'SI001',
    address: 'ABC Street',
    plant: 'Paddy',
    status: 'Active',
}
const FarmContent = () => {
  const [isWateringOn, setIsWateringOn] = useState(false);
  const [isFanOn, setIsFanOn] = useState(false);
  const [isLightOn, setIsLightOn] = useState(false);
  const [solution1, setSolution1] = useState(false);
  const [solution2, setSolution2] = useState(false);
  const [solution3, setSolution3] = useState(false);
  const [showChart, setShowChart] = useState('temp');
  const [selectedTab, setSelectedTab] = useState('manual');

  const toggleCheckbox = (setFunction, value) => {
    setFunction(!value);
  };

  const temp = [20, 21, 29, 22, 20, 23, 21];
  const humid = [60, 65, 63, 62, 64, 66, 61];
  const light = [57, 14, 50, 15, 42, 33, 94];
  const pH = [7.45, 8.31, 7.62, 7.41, 8.10, 8.26, 6.99];

  const data = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
        {
          data: showChart === 'temp' ? temp 
               : showChart === 'humid' ? humid 
               : showChart === 'light' ? light 
               : pH, 
          color: (opacity = 1) => showChart === 'temp' ? `red` 
                : showChart === 'humid' ? `blue` 
                : showChart === 'light' ? `#fcba03` 
                : `#299483`, 
          strokeWidth: 3,
        },
        {
          data: [showChart === 'temp' ? 15 
               : showChart === 'humid' ? 50 
               : showChart === 'light' ? 0 
               : 3], // Min giá trị của từng loại
          withDots: false,
        },
        {
          data: [showChart === 'temp' ? 35 
               : showChart === 'humid' ? 70 
               : showChart === 'light' ? 100 
               : 10], // Max giá trị của từng loại
          withDots: false,
        },
      ],
      legend: [showChart === 'temp' ? 'Temperature (°C)' 
             : showChart === 'humid' ? 'Humidity (%)' 
             : showChart === 'light' ? 'Light (Klux)' 
             : 'pH'],
    };

  const chartConfig = {
    backgroundGradientFrom: '#216923',
    backgroundGradientTo: '',
    decimalPlaces: showChart === 'pH' ? 2 : 0,
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    style: {
      borderRadius: 15,
    },
    propsForDots: {
      r: '0',
      strokeWidth: '2',
    },
  };

  return (
    <ScrollView style={styles.container}>
    <View style={styles.container_sub}>
      <Text style={styles.title1}>INFORMATIONS</Text>
      <Text style={styles.label}>NAME: <Text style={styles.name}>{farm1.name}</Text></Text>
      <Text style={styles.label}>ID: <Text style={styles.name}>{farm1.ID}</Text></Text>
      <Text style={styles.label}>ADDRESS: <Text style={styles.name}>{farm1.address}</Text></Text>
      <Text style={styles.label}>PLANT: <Text style={styles.name}>{farm1.plant}</Text></Text>
      <Text style={styles.label}>STATUS: <Text style={[styles.name, farm1.status === 'Active' ? styles.active : styles.inactive]}>{farm1.status}</Text></Text>
    </View>

    <View style={styles.container_sub}>
    <Text style={styles.title1}>PARAMETERS</Text>
      {showChart && (
        <LineChart
          data={data}
          width={screenWidth - 60}
          height={220}
          chartConfig={chartConfig}
          bezier
          style={{
            marginVertical: 10,
            borderRadius: 15,
          }}
        />
      )}

        <View style={styles.buttonRow}>
            <Pressable style={[styles.button, styles.red]} onPress={() => setShowChart('temp')}>
            <Text style={styles.buttonText}>Temperature</Text>
            <Text style={styles.buttonText}>{temp[6]}°C</Text>
            </Pressable>

            <Pressable style={[styles.button, styles.blue]} onPress={() => setShowChart('humid')}>
            <Text style={styles.buttonText}>Humidity</Text>
            <Text style={styles.buttonText}>{humid[6]}%</Text>
            </Pressable>
        </View>
        <View style={styles.buttonRow}>
            <Pressable style={[styles.button, styles.yellow]} onPress={() => setShowChart('light')}>
            <Text style={styles.buttonText}>Light</Text>
            <Text style={styles.buttonText}>{light[6]} Klux</Text>
            </Pressable>

            <Pressable style={[styles.button, styles.gray]} onPress={() => setShowChart('pH')}>
            <Text style={styles.buttonText}>pH</Text>
            <Text style={styles.buttonText}>{pH[6]}</Text>
            </Pressable>
        </View>
      </View>

      <View style={styles.container_sub}>
        <Text style={styles.title1}>SELECT MODE</Text>

        <View style={styles.tabContainer}>
        <Pressable
          style={[styles.tab, selectedTab === 'manual' && styles.activeTab]}
          onPress={() => setSelectedTab('manual')}
        >
          <Text style={[styles.tabButtonText, selectedTab === 'manual' && styles.textActive]}>MANUAL</Text>
        </Pressable>
        <Pressable
          style={[styles.tab, selectedTab === 'automatic' && styles.activeTab]}
          onPress={() => setSelectedTab('automatic')}
        >
          <Text style={[styles.tabButtonText, selectedTab === 'automatic' && styles.textActive]}>AUTOMATIC</Text>
        </Pressable>
      </View>

      {selectedTab === 'manual' && (
        <View style={styles.section}>
          <View style={styles.switchContainer}>
            <Text>Watering Machine 1</Text>
            <Switch
              value={isWateringOn}
              onValueChange={setIsWateringOn}
            />
          </View>
          <View style={styles.switchContainer}>
            <Text>Watering Machine 2</Text>
            <Switch
              value={isWateringOn}
              onValueChange={setIsWateringOn}
            />
          </View>
          <View style={styles.switchContainer}>
            <Text>Watering Machine 3</Text>
            <Switch
              value={isWateringOn}
              onValueChange={setIsWateringOn}
            />
          </View>
          <View style={styles.switchContainer}>
            <Text>Fan</Text>
            <Switch
              value={isFanOn}
              onValueChange={setIsFanOn}
            />
          </View>
          <View style={styles.switchContainer}>
            <Text>Light</Text>
            <Switch
              value={isLightOn}
              onValueChange={setIsLightOn}
            />
          </View>

          <Text style={styles.label}>Solutions</Text>
            <View style={styles.checkboxContainer}>
            <Pressable onPress={() => toggleCheckbox(setSolution1, solution1)} style={styles.checkbox}>
                {solution1 && <View style={styles.checked} />}
            </Pressable>
            <Text>Solution 1</Text>
            </View>
            <View style={styles.checkboxContainer}>
            <Pressable onPress={() => toggleCheckbox(setSolution2, solution2)} style={styles.checkbox}>
                {solution2 && <View style={styles.checked} />}
            </Pressable>
            <Text>Solution 2</Text>
            </View>
            <View style={styles.checkboxContainer}>
            <Pressable onPress={() => toggleCheckbox(setSolution3, solution3)} style={styles.checkbox}>
                {solution3 && <View style={styles.checked} />}
            </Pressable>
            <Text>Solution 3</Text>
            </View>
        </View>
      )}

      {selectedTab === 'automatic' && (
      <View style={styles.section}>
      </View>
      )}
    </View>
    <Pressable style={styles.button1} onPress={() => alert('Saved!')}>
        <Text style={styles.buttonText}>Apply Changes</Text>
    </Pressable>
      <View style={styles.spaceEnd}></View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: '#f5f5f5',
  },
  container_sub: {
    flex: 1,
    paddingLeft: 20,
    backgroundColor: '#f5f5f5',
    borderBottomColor: 'gray',
    borderBottomWidth: 1,
    marginBottom: 20,
  },
  title1: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    marginLeft: -20,
    fontStyle: 'italic',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  section: {
    marginBottom: 20,
    width: '95%',
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  name: {
    fontSize: 16,
    fontWeight: 'normal',
  },
  active: {
    color: 'green',
    fontWeight: 'bold',
  },
  inactive: {
    color: 'red',
    fontWeight: 'bold',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    backgroundColor: '#fff',
  },
  switchContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 1,
    borderColor: '#ccc',
    marginRight: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checked: {
    width: 14,
    height: 14,
    backgroundColor: '#0074FF',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '95%',
    marginBottom: 15,
  },
  button: {
    padding: 10,
    alignItems: 'center',
    width: '48%',
    borderRadius: 15,
  },
  button1: {
    paddingHorizontal: 25,
    paddingVertical: 15,
    borderRadius: 10,
    backgroundColor: '#0074FF',
    alignSelf: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    marginTop: 2,
    marginBottom: 2,
  },
  red: {
    backgroundColor: 'red',
  },
  blue: {
    backgroundColor: 'blue',
  },
  yellow: {
    backgroundColor: '#e8ab02',
  },
  green: {
    backgroundColor: 'green',
  },
  cyan: {
    backgroundColor: '#0074FF',
  },
  gray: {
    backgroundColor: '#299483',
  },
  tabContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
    width: '95%',
  },
  tab: {
    flex: 1,
    padding: 10,
    alignItems: 'center',
    borderBottomWidth: 3,
    borderBottomColor: 'transparent',
    borderBottomColor: '#ccc',
  },
  activeTab: {
    borderBottomColor: '#059033',
    backgroundColor: '#C8E6C9',
  },
  textActive: {
    color: 'green',
  },
  tabButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'gray',
  },
  spaceEnd: {
    height: 50,
  },
  picker: {
    width: '100%',
  },
  dropdownButton: {
    width: '100%',
    height: 50,
    backgroundColor: '#fff',
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#ccc',
    marginBottom: 20,
  },
  dropdownButtonText: {
    textAlign: 'left',
    marginLeft: 10,
    fontSize: 16,
  },
  dropdown: {
    borderRadius: 5,
  },
  dropdownRow: {
    height: 40,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  dropdownRowText: {
    textAlign: 'left',
    marginLeft: 10,
    fontSize: 16,
  },
});

export default FarmContent;