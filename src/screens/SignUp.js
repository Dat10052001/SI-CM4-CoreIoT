import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Pressable,
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard,
} from 'react-native';
import { signupStyles } from '../../styles';

const Signup = () => {
  const [getPasswordViaPhone, setGetPasswordViaPhone] = useState(false);
  const [getPasswordViaEmail, setGetPasswordViaEmail] = useState(false);
  const [selectedTab, setSelectedTab] = useState('signup');

  const handleSignup = () => {
    // Handle signup logic here
  };

  const handleResetPassword = () => {
    // Handle password reset logic here
  };

  const toggleGetPasswordViaPhone = () => {
    setGetPasswordViaPhone(!getPasswordViaPhone);
    if (!getPasswordViaPhone) {
      setGetPasswordViaEmail(false);
    }
  };

  const toggleGetPasswordViaEmail = () => {
    setGetPasswordViaEmail(!getPasswordViaEmail);
    if (!getPasswordViaEmail) {
      setGetPasswordViaPhone(false);
    }
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View style={{ flex: 1 }}>
          <View style={signupStyles.tabContainer}>
            <TouchableOpacity
              style={[signupStyles.tab, selectedTab === 'signup' && signupStyles.activeTab]}
              onPress={() => setSelectedTab('signup')}
            >
              <Text style={signupStyles.tabText}>Sign Up</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[signupStyles.tab, selectedTab === 'reset' && signupStyles.activeTab]}
              onPress={() => setSelectedTab('reset')}
            >
              <Text style={signupStyles.tabText}>Reset Password</Text>
            </TouchableOpacity>
          </View>
          <ScrollView contentContainerStyle={signupStyles.container}>
            {selectedTab === 'signup' && (
              <>
                <Text style={signupStyles.title}>Sign up for using service</Text>
                <TextInput style={signupStyles.input} placeholder="Last Name" />
                <TextInput style={signupStyles.input} placeholder="First Name" />
                <TextInput style={signupStyles.input} placeholder="ID" keyboardType="numeric" />
                <TextInput style={signupStyles.input} placeholder="Phone Number" keyboardType="numeric" />
                <TextInput style={signupStyles.input} placeholder="Address" />
                <TextInput style={signupStyles.input} placeholder="Email" keyboardType="email-address" />

                <TouchableOpacity onPress={handleSignup}>
                  <Text style={signupStyles.signup_btn}>Sign Up</Text>
                </TouchableOpacity>
              </>
            )}

            {selectedTab === 'reset' && (
              <>
                <Text style={signupStyles.title}>Reset Password</Text>
                <TextInput style={signupStyles.input} placeholder="Phone Number" keyboardType="numeric" />
                <TextInput style={signupStyles.input} placeholder="Email" keyboardType="email-address" />
                <TextInput style={signupStyles.input} placeholder="Contract number" />

                <View style={signupStyles.checkboxContainer}>
                  <Pressable
                    onPress={toggleGetPasswordViaPhone}
                    style={[signupStyles.checkbox, getPasswordViaPhone && signupStyles.checkboxChecked]}
                  >
                    {getPasswordViaPhone && <Text style={signupStyles.checkboxText}></Text>}
                  </Pressable>
                  <Text style={signupStyles.label}>Get new password via phone number</Text>
                </View>

                <View style={signupStyles.checkboxContainer}>
                  <Pressable
                    onPress={toggleGetPasswordViaEmail}
                    style={[signupStyles.checkbox, getPasswordViaEmail && signupStyles.checkboxChecked]}
                  >
                    {getPasswordViaEmail && <Text style={signupStyles.checkboxText}></Text>}
                  </Pressable>
                  <Text style={signupStyles.label}>Get new password via email</Text>
                </View>

                <TouchableOpacity onPress={handleResetPassword}>
                  <Text style={signupStyles.reset_btn}>Reset Password</Text>
                </TouchableOpacity>
              </>
            )}
          </ScrollView>
        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};

export default Signup;