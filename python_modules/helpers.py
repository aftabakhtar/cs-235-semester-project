from scipy.signal import butter, lfilter, freqz


def butter_lowpass(cutoff, fs, order=6):
	nyq = 0.5 * fs
	normal_cutoff = cutoff / nyq
	b, a = butter(order, normal_cutoff, btype='low', analog=False)
	return b, a


def butter_lowpass_filter(data, cutoff=3.667, fs=30, order=6):
	b, a = butter_lowpass(cutoff, fs, order=order)
	y = lfilter(b, a, data)
	return y


def plot_data(ax, x, data_, gradient_, butterworth_smoothing=False):
	"""
	data_ - as passed by read_socket()
	"""
	last = 50


	if len(data_['Ax']) > 1:
		# x = [j for j in range(len(data_['Ax']))]
		d = dict()
		g = dict()
		if butterworth_smoothing:
			for key in data_:
				d[key] = butter_lowpass_filter(data_[key][-last:], cutoff=2.5)
				g[key] = butter_lowpass_filter(gradient_[key][-last:], cutoff=1.0)
		else:
			g = gradient_
			d = data_

		for x_ in x[-last:]:
			if (d['Gx'][x_] > 15 and d['Gz'][x_] < -15 and
				g['Ax'][x_] < -0.0075 and g['Gx'][x_] > 0.75
				and g['Gy'][x_] < -0.25 and g['Gz'][x_] < -0.25):
				print("Bump detected at x =", x_)

		ax[0][0].plot(x[-last:], d['Ax'][-last:])
		ax[0][0].plot(x[-last:], d['Ay'][-last:])
		ax[0][0].plot(x[-last:], d['Az'][-last:])
		ax[0][0].legend(['x', 'y', 'z'])
		ax[0][0].set_title('Accelerometer', fontdict={'fontsize':12})

		ax[0][1].plot(x[-last:], d['Gx'][-last:])
		ax[0][1].plot(x[-last:], d['Gy'][-last:])
		ax[0][1].plot(x[-last:], d['Gz'][-last:])
		ax[0][1].legend(['x', 'y', 'z'])
		ax[0][1].set_title('Gyroscope', fontdict={'fontsize':12})

		ax[1][0].plot(x[-last:], g['Ax'][-last:])
		ax[1][0].plot(x[-last:], g['Ay'][-last:])
		ax[1][0].plot(x[-last:], g['Az'][-last:])
		# ax[1][1].set_title('Gyroscope Gradients', fontdict={'fontsize':8})

		ax[1][1].plot(x[-last:], g['Gx'][-last:])
		ax[1][1].plot(x[-last:], g['Gy'][-last:])
		ax[1][1].plot(x[-last:], g['Gz'][-last:])
		# ax[1][0].set_title('Accelerometer Gradients', fontdict={'fontsize':8})