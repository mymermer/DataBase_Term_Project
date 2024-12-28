import React, { useState, useEffect, forwardRef } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import styles from '../styles/DateTimeInput.module.css';

// Custom input component to render the time input field
const CustomInput = forwardRef(({ value, onClick }, ref) => (
  <input
    className={styles.timeInput}
    onClick={onClick}
    ref={ref}
    value={value || '__:__'}
    readOnly
  />
));

const TimeInput = ({ value, onChange, placeholder }) => {
  const [selectedTime, setSelectedTime] = useState(value ? new Date(`1970-01-01T${value}:00`) : null);

  useEffect(() => {
    setSelectedTime(value ? new Date(`1970-01-01T${value}:00`) : null);
  }, [value]);

  const handleChange = (time) => {
    setSelectedTime(time);
    if (time) {
      const formattedTime = time.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      });
      onChange(formattedTime);
    } else {
      onChange('');
    }
  };

  return (
    <div className={styles.timeInputWrapper}>
      <DatePicker
        selected={selectedTime}
        onChange={handleChange}
        showTimeSelect
        showTimeSelectOnly
        timeIntervals={15}
        timeFormat="HH:mm"
        dateFormat="HH:mm"
        customInput={<CustomInput />}
        popperClassName={styles.timePickerPopper}
        timeClassName={() => styles.timePickerTime}
        className={styles.timePicker}
      />
    </div>
  );
};

export default TimeInput;
