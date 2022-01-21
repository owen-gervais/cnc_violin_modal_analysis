if (TARGET tinyusb_device)
	add_executable(controller
			controller.cpp
			pwm.cpp
			motor.cpp
			encoder.cpp
			)

	target_link_libraries(controller
			pico_stdlib
			hardware_adc
			hardware_dma
			hardware_pwm
			hardware_pio
			)

	# enable usb output, disable uart output
	pico_enable_stdio_usb(controller 1)
	pico_enable_stdio_uart(controller 0)

	# create map/bin/hex file etc.
	pico_add_extra_outputs(controller)

	# add url via pico_set_program_url
	example_auto_set_url(controller)
elseif(PICO_ON_DEVICE)
	message(WARNING "not building dma_capture because TinyUSB submodule is not initialized in the SDK")
endif()