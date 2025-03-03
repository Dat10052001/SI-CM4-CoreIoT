import React, { useState } from 'react';
import { View, Text, Switch, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';

const Control = props => {
  const [fan, setFAN] = useState(false);
  const toggleFAN = (value) => {
    setFAN(value);
  };

  const [light, setLIGHT] = useState(false);
  const toggleLIGHT = (value) => {
    setLIGHT(value);
  };

  const sendSignalLight1 = async (light1) => {
    try {
      let lightsignal = light1 ? 1 : 0;
      const response = await fetch(``, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-AIO-Key': IO_KEY
        },
        body: JSON.stringify({ value: lightsignal })
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  };

  const sendSignalFan = async (fan) => {
    try {
      let fansignal = fan ? 1 : 0;
      const response = await fetch(``, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-AIO-Key': IO_KEY
        },
        body: JSON.stringify({ value: fansignal })
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View>
      <View style={styles.header}>
        <Text style={{ fontSize: 24, color: 'white', fontWeight: 'bold' }}>
          Control
        </Text>
      </View>
      <View>
        <View style={styles.control}>
          <View style={styles.button}>
            <Text style={{ fontSize: 20 }}>
              <Icon name='fan' size={20} />{"   "}SMART FAN
            </Text>
            <Text style={styles.on_off}>{fan ? 'ON' : 'OFF'}</Text>
            <Switch
              style={{ marginTop: 50, marginLeft: 100 }}
              onValueChange={toggleFAN}
              value={fan}
              onGestureEvent={sendSignalFan(fan)}
            />
          </View>
        </View>

        <View style={styles.control}>
          <View style={styles.button}>
            <Text style={{ fontSize: 20 }}>
              <Icon name='lightbulb' size={20} />{"   "}SMART LIGHT
            </Text>
            <Text style={styles.on_off}>{light ? 'ON' : 'OFF'}</Text>
            <Switch
              style={{ marginTop: 50, marginLeft: 100 }}
              onValueChange={toggleLIGHT}
              value={light}
              onGestureEvent={sendSignalLight1(light)}
            />
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    width: 1000,
    height: 100,
    backgroundColor: '#3f6ff0',
    justifyContent: 'center',
    paddingLeft: 50,
    marginBottom: 30
  },
  control: {
    backgroundColor: '#059033',
    marginTop: 10,
    marginBottom: 50,
    width: 250,
    left: 90,
    borderColor: '#059033',
    borderWidth: 1,
    borderRadius: 15
  },
  button: {
    justifyContent: 'center',
    alignItems: 'center',
    margin: 25,
    marginBottom: 15
  },
  on_off: {
    top: 80,
    left: 25,
    position: 'absolute',
    fontSize: 20,
    fontWeight: 'bold'
  }
});

export default Control;