import React from 'react';
import {
  View,
  Text,
  Image,
  ImageBackground,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';

const Start = props => {
  const change = () => {
    props.navigation.navigate('LOGIN');
  };

  return (
    <ImageBackground 
      source={require("../assets/banner.jpg")} 
      style={styles.background}
      resizeMode="cover"
    >
      <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
        <Image source={require("../assets/logo.png")} style={{width: 250, height: 250}}/>
        <Text style={styles.title}>LET MAKE YOUR FARM !</Text>
        <TouchableOpacity onPress={change}>
          <Text style={styles.start_btn}>GET STARTED</Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 80,
    marginTop: 0,
    color: 'darkgreen',
  },
  start_btn: {
    padding: 10,
    paddingLeft: 20,
    paddingRight: 20,
    borderWidth: 1,
    borderColor: '#059033',
    borderRadius: 15,
    color: 'white',
    fontSize: 20,
    backgroundColor: '#059033',
    overflow: 'hidden',
  },
});

export default Start;