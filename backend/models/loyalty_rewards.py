"""
Loyalty Points Manager for Flask Application
"""
import mysql.connector
from datetime import datetime

class LoyaltyManager:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def get_connection(self):
        """Create database connection"""
        return mysql.connector.connect(**self.db_config)
    
    def get_balance(self, customer_id):
        """Get customer's loyalty point balance"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT total_points, lifetime_points, created_at
                FROM loyalty_accounts
                WHERE customer_id = %s
            """, (customer_id,))
            
            result = cursor.fetchone()
            
            if not result:
                # Create account if doesn't exist
                cursor.execute("""
                    INSERT INTO loyalty_accounts (customer_id, total_points, lifetime_points)
                    VALUES (%s, 0, 0)
                """, (customer_id,))
                conn.commit()
                return {'total_points': 0, 'lifetime_points': 0}
            
            return result
        finally:
            cursor.close()
            conn.close()
    
    def award_points(self, customer_id, order_id, order_total):
        """Award points when order is completed"""
        # Calculate points: 1 point per dollar spent
        points_earned = int(order_total)
        
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()
            
            # Create or update loyalty account
            cursor.execute("""
                INSERT INTO loyalty_accounts (customer_id, total_points, lifetime_points)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    total_points = total_points + %s,
                    lifetime_points = lifetime_points + %s
            """, (customer_id, points_earned, points_earned, points_earned, points_earned))
            
            # Get new balance
            cursor.execute("""
                SELECT total_points FROM loyalty_accounts WHERE customer_id = %s
            """, (customer_id,))
            balance = cursor.fetchone()['total_points']
            
            # Record transaction
            cursor.execute("""
                INSERT INTO loyalty_transactions
                (customer_id, order_id, points_change, transaction_type, description, balance_after)
                VALUES (%s, %s, %s, 'earned', %s, %s)
            """, (customer_id, order_id, points_earned, f"Earned from Order #{order_id}", balance))
            
            # Update order record
            cursor.execute("""
                UPDATE orders SET loyalty_points_earned = %s WHERE id = %s
            """, (points_earned, order_id))
            
            conn.commit()
            return points_earned
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def get_available_rewards(self, customer_id):
        """Get all rewards with redemption status"""
        balance = self.get_balance(customer_id)
        
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT *,
                    CASE WHEN points_required <= %s THEN 1 ELSE 0 END as can_redeem
                FROM rewards
                WHERE is_active = TRUE
                ORDER BY points_required ASC
            """, (balance['total_points'],))
            
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def redeem_reward(self, customer_id, reward_id):
        """Redeem points for a reward"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()
            
            # Get reward details
            cursor.execute("""
                SELECT * FROM rewards WHERE id = %s AND is_active = TRUE
            """, (reward_id,))
            reward = cursor.fetchone()
            
            if not reward:
                raise ValueError("Reward not found or inactive")
            
            # Check balance
            balance = self.get_balance(customer_id)
            if balance['total_points'] < reward['points_required']:
                raise ValueError("Insufficient points")
            
            # Deduct points
            cursor.execute("""
                UPDATE loyalty_accounts
                SET total_points = total_points - %s
                WHERE customer_id = %s
            """, (reward['points_required'], customer_id))
            
            # Get new balance
            new_balance = self.get_balance(customer_id)
            
            # Record transaction
            cursor.execute("""
                INSERT INTO loyalty_transactions
                (customer_id, points_change, transaction_type, description, balance_after)
                VALUES (%s, %s, 'redeemed', %s, %s)
            """, (
                customer_id,
                -reward['points_required'],
                f"Redeemed: {reward['name']}",
                new_balance['total_points']
            ))
            
            conn.commit()
            
            return {
                'discount_type': reward['discount_type'],
                'discount_value': float(reward['discount_value']),
                'points_redeemed': reward['points_required'],
                'reward_name': reward['name']
            }
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def apply_discount_to_order(self, order_id, discount_info):
        """Apply redeemed discount to order"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE orders
                SET discount_type = %s,
                    discount_amount = %s,
                    loyalty_points_redeemed = %s
                WHERE id = %s
            """, (
                discount_info['discount_type'],
                discount_info['discount_value'],
                discount_info['points_redeemed'],
                order_id
            ))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    
    def get_transaction_history(self, customer_id, limit=20):
        """Get customer's points transaction history"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT *
                FROM loyalty_transactions
                WHERE customer_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (customer_id, limit))
            
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()