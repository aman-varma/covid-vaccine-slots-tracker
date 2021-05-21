package com.vaccine.notification.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vaccine.notification.entity.User;
import com.vaccine.notification.service.UserService;

@Controller
@RequestMapping("/home")
public class ApplicationController {

	@Autowired	
	private UserService userService;
	
	List<User> userList = new ArrayList<User>();
	
	@GetMapping("/register")
	public String registerUsers(Model model) {
		
		//List<Employee> employees = userService.findAll();
		// add to the spring model
		//theModel.addAttribute("employees", employees);
		User user = new User();
		model.addAttribute("user", user);
		return "/usr/register";
	}
	
	@GetMapping("/de-register")
	public String deregisterUser(Model model) {
		
		//List<Employee> employees = userService.findAll();
		// add to the spring model
		//theModel.addAttribute("employees", employees);
		//String email = "";
		User user = new User();
		model.addAttribute("user", user);
		//model.addAttribute("email", email);
		return "/usr/de-register";
	}
/*	@GetMapping("/showFormForAdd")
	public String showFormForAdd(Model model) {
		
		User user = new User();
		model.addAttribute("employee", user);
		
		return "/employees/employee-form";
	}
*/	
	@PostMapping("/save")
	public String saveUser(@ModelAttribute("user") User user) {
		userService.save(user);
//		userList.add(user);
		return "/usr/user-page";
	}
	
/*	@GetMapping("/userPage")
	public String showUserPage(Model model) {
			
		return "redirect:/home/register";
	
	}
*/	
	@GetMapping("/showFormForUpdate")
	public String showFormForUpdate(@RequestParam("id") int id, Model model) {
		
		User user = userService.findById(id);
		model.addAttribute("user", user);
		return "/usr/edit-user";
	}

	@GetMapping("/delete")
	public String delete(@RequestParam("email") String email ) {

		List<User> allUsers = userService.findAll();
		for (User user : allUsers) {
			if( user.getEmail().equals(email)) {
				userService.deleteById(user.getId());
			}
		}
		
		return "usr/redirect";
	}

	
}











