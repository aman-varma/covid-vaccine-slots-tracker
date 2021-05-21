package com.vaccine.notification.dao;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.vaccine.notification.entity.User;

public interface UserRepository extends JpaRepository< User, Integer> {

//	public List<User> findAllByOrderByLastNameAsc();

}
