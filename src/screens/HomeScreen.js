import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';
import styles from '../../styles'; // Adjust the import based on your styles file location

const HomeScreen = props => {
  // GO TO CONTROL SCREEN
  const control = () => {
    props.navigation.navigate('CONTROL');
  };
  // GO TO DATA SCREEN
  const data = () => {
    props.navigation.navigate('DATA');
  };
  // GO TO OPEN DOOR SCREEN
  const door = () => {
    props.navigation.navigate('OTHERS');
  };
  
  return (
    <View> 
      {/* HEADER */}
      <View style={styles.header}>
        <Text style={{ fontSize: 24, color: 'white', fontWeight: 'bold' }}>
          Hello , USER 
        </Text>
      </View>
      
      <View>
        {/* CONTROL */}
        <TouchableOpacity style={styles.button} onPress={control}>
          <Text style={styles.f_button}>
            <Icon name='adjust' size={15}/>
            {"   "}CONTROL
          </Text>
        </TouchableOpacity>
        {/* DATA */}
        <TouchableOpacity style={styles.button} onPress={data}>
          <Text style={styles.f_button}>
            <Icon name='database' size={15}/>
            {"   "}DATA
          </Text>
        </TouchableOpacity>
        {/* OPEN DOOR*/}
        <TouchableOpacity style={styles.button} onPress={door}>
          <Text style={styles.f_button}>
            <Icon name='door-open' size={15}/>
            {"   "}OPEN DOOR
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default HomeScreen;