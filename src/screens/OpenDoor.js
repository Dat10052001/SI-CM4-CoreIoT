import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';
import { styles } from '../../styles'; // Adjust the import based on your styles file location

const OpenDoor = props => {
  const [door, setDoor] = useState("");

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:3000/ws');
    socket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      setDoor(data.door === "1" ? "Open" : "Close");
    };
    return () => socket.close();
  }, []);

  const sendSignalDoor = async () => {
    try {
      let doorsignal = "4";
      const response = await fetch(``, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-AIO-Key': IO_KEY
        },
        body: JSON.stringify({ value: doorsignal })
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
          OPEN DOOR
        </Text>
      </View>
      <TouchableOpacity style={styles.button} onPress={sendSignalDoor}>
        <Text style={styles.f_button}>
          <Icon name='adjust' size={15} />
          {"   "}CHECK BY FACE
        </Text>
      </TouchableOpacity>
      <View style={styles.button}>
        <Text style={styles.f_button}>
          <Icon name='door-closed' size={15} />
          {"   "}DOOR'S STATE{"\n\n"}
          <Text style={{ fontWeight: 'bold' }}>
            {door}
          </Text>
        </Text>
      </View>
    </View>
  );
};

export default OpenDoor;