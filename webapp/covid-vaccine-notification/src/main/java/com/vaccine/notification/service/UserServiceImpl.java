package com.vaccine.notification.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.vaccine.notification.dao.UserRepository;
import com.vaccine.notification.entity.User;

@Service
public class UserServiceImpl implements UserService {

	@Autowired
	private UserRepository userRepository;
	
	@Override
	@Transactional
	public List<User> findAll() {
		return userRepository.findAll();
	}

	@Override
	@Transactional
	public User findById(int id) { 
		User user = null;
		Optional<User> result = userRepository.findById(id);
		if (result.isPresent()) {
			user = result.get();
		}
		else
			throw new RuntimeException("User ID not found: " + id);
		return user;
	}

	@Override
	@Transactional
	public void save(User user) {
		userRepository.save(user);
	}

	@Override
	@Transactional
	public void deleteById(int id) {
		userRepository.deleteById(id);
	}


}
