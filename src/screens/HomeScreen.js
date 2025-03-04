import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';
import { loginStyles } from '../../styles';

const HomeScreen = props => {
  // GO TO CONTROL SCREEN
  const control = () => {
    props.navigation.navigate('CONTROL');
  };
  // GO TO DATA SCREEN
  const data = () => {
    props.navigation.navigate('DATA');
  };

  return (
    <View> 
      {/* HEADER */}
      <View style={loginStyles.header}>
        <Text style={{ fontSize: 24, color: 'white', fontWeight: 'bold' }}>
          Hello , USER 
        </Text>
      </View>
      
      <View>
        {/* CONTROL */}
        <TouchableOpacity style={loginStyles.button} onPress={control}>
          <Text style={loginStyles.f_button}>
            <Icon name='adjust' size={15}/>
            {"   "}CONTROL
          </Text>
        </TouchableOpacity>
        {/* DATA */}
        <TouchableOpacity style={loginStyles.button} onPress={data}>
          <Text style={loginStyles.f_button}>
            <Icon name='database' size={15}/>
            {"   "}DATA
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default HomeScreen;