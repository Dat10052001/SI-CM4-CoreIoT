import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';

const Data = props => {
  const [temp, setTemp] = useState(0);
  const [light, setLight] = useState(0);
  const [humid, setHumid] = useState(0);
  const [door, setDoor] = useState("");

  useEffect(() => {
    socket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      setTemp(data.temp);
      setHumid(data.humid);
      setLight(data.light);
      setDoor(data.door === "1" ? "Open" : "Close");
    };
  }, []);

  return (
    <View>
      <View style={styles.header}>
        <Text style={{ fontSize: 24, color: 'white', fontWeight: 'bold' }}>
          DATA
        </Text>
      </View>
      <View>
        <View style={styles.button}>
          <Text style={styles.f_button}>
            <Icon name='temperature-high' size={15} />
            {"   "}TEMPERATURE{"\n\n"}
            <Text style={{ fontWeight: 'bold' }}>
              {temp}°C
            </Text>
          </Text>
        </View>
        <View style={styles.button}>
          <Text style={styles.f_button}>
            <Icon name='lightbulb' size={15} />
            {"   "}LIGHT{"\n\n"}
            <Text style={{ fontWeight: 'bold' }}>
              {light}%
            </Text>
          </Text>
        </View>
        <View style={styles.button}>
          <Text style={styles.f_button}>
            <Icon name='water' size={15} />
            {"   "}HUMIDITY{"\n\n"}
            <Text style={{ fontWeight: 'bold' }}>
              {humid}%
            </Text>
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    width: '100%',
    height: 100,
    backgroundColor: '#3f6ff0',
    justifyContent: 'center',
    paddingLeft: 50,
    marginBottom: 30,
  },
  button: {
    justifyContent: 'center',
    alignItems: 'center',
    margin: 25,
    marginBottom: 15,
  },
  f_button: {
    paddingVertical: 20,
    borderWidth: 1,
    borderColor: '#059033',
    borderRadius: 15,
    fontSize: 20,
    backgroundColor: '#059033',
    overflow: 'hidden',
    width: 250,
    textAlign: "center",
  },
});

export default Data;