import React, { useState } from 'react';
import { 
  View, Text, TextInput, Alert, StyleSheet, Image, KeyboardAvoidingView, Keyboard, Platform,
  TouchableWithoutFeedback, TouchableOpacity } from 'react-native'
import Icon from 'react-native-vector-icons/FontAwesome5';

const Account = ({navigation}) => {
  const [name, setName] = useState('Huynh Tan Dat');
  const [phoneNumber, setPhoneNumber] = useState('0123456789');
  const [email, setEmail] = useState('dat@gmail.com');
  const [password, setPassword] = useState('12345678');
  const [address, setAddress] = useState('123 ABC, District 7, Ho Chi Minh City');
  const [isEditing, setIsEditing] = useState(false);
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const handleEditAvatar = () => {
    Alert.alert('Edit Avatar', 'You can choose to take a photo or select a photo from your gallery.');
  };

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View style={styles.container}>
          <View style={styles.avatarContainer}>
            <Image source={require("../assets/avatar_sample.jpg")} style={styles.avatar} />
            <TouchableOpacity style={styles.editAvatarButton} onPress={handleEditAvatar}>
              <Icon name="camera" color={'white'} size={20} />
            </TouchableOpacity>
          </View>
          <Text style={styles.inputTitle}>Full name</Text>
          <TextInput
            style={[styles.input, isEditing ? styles.inputEnabled : styles.inputDisabled]}
            placeholder="Name"
            value={name}
            onChangeText={setName}
            editable={isEditing}
          />
          <Text style={styles.inputTitle}>Phone number</Text>
          <TextInput
            style={[styles.input, isEditing ? styles.inputEnabled : styles.inputDisabled]}
            placeholder="Phone Number"
            keyboardType="phone-pad"
            value={phoneNumber}
            onChangeText={setPhoneNumber}
            editable={isEditing}
          />
          <Text style={styles.inputTitle}>Email</Text>
          <TextInput
            style={[styles.input, isEditing ? styles.inputEnabled : styles.inputDisabled]}
            placeholder="Email"
            keyboardType="email-address"
            value={email}
            onChangeText={setEmail}
            editable={isEditing}
          />
          <Text style={styles.inputTitle}>Address</Text>
          <TextInput
            style={[styles.input, isEditing ? styles.inputEnabled : styles.inputDisabled]}
            placeholder="Address"
            value={address}
            onChangeText={setAddress}
            editable={isEditing}
          />
          <Text style={[styles.inputTitle, {marginBottom: -30}]}>Password</Text>
          <View style={styles.passwordContainer}>
            <TextInput
              style={[styles.input, styles.inputDisabled]}
              placeholder="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!isPasswordVisible}
              editable={false}
            />
            <TouchableOpacity onPress={togglePasswordVisibility} style={styles.passwordToggle}>
              <Icon name={!isPasswordVisible ? 'eye' : 'eye-slash'} size={20} color="gray" />
            </TouchableOpacity>
          </View>
          <TouchableOpacity style={styles.editButton} onPress={() => setIsEditing(!isEditing)}>
            <View style={styles.editButtonContent}>
              <Text style={styles.editButtonText}>{isEditing ? 'Save' : 'Edit'}</Text>
              <Icon name={isEditing ? 'save' : 'edit'} color={'white'} size={20} style={styles.editButtonIcon} />
            </View>
          </TouchableOpacity>
        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    //justifyContent: 'center',
    alignItems: 'center',
  },
  avatarContainer: {
    position: 'relative',
  },
  avatar: {
    width: 150,
    height: 150,
    borderRadius: 75,
    margin: 20,
  },
  editAvatarButton: {
    position: 'absolute',
    bottom: 30,
    right: 30,
    backgroundColor: 'blue',
    borderRadius: 15,
    padding: 5,
  },
  input: {
    width: '80%',
    padding: 10,
    marginVertical: 15,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    fontSize: 16,
    paddingLeft: 15,
  },
  inputTitle: {
    alignSelf: 'flex-start',
    marginLeft: '10%',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: -15,
  },
  inputEnabled: {
    borderColor: '#000',
    backgroundColor: '#fff',
  },
  inputDisabled: {
    borderColor: '#ccc',
    backgroundColor: '#f0f0f0',
  },
  logoutButton: {
    backgroundColor: 'blue',
    padding: 15,
    borderRadius: 15,
    marginTop: 25,
  },
  logoutButtonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: 18,
  },
  logoutButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoutButtonIcon: {
    marginLeft: 10,
  },
  editButton: {
    backgroundColor: '#0074FF',
    padding: 15,
    borderRadius: 15,
    marginTop: 25,
  },
  editButtonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: 18,
  },
  editButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  editButtonIcon: {
    marginLeft: 10,
  },
  passwordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '120%',
    marginVertical: 15,
    paddingLeft: '20%',
  },
  passwordToggle: {
    position: 'absolute',
    right: 90,
  },
});

export default Account;